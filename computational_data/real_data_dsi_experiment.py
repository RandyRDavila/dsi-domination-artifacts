#!/usr/bin/env python3
"""Real-data pilot experiment for DSI-selected ensemble members.

The experiment uses small standard classification datasets and only the
Python standard library.  For each train/validation/test split, it trains a
pool of simple base learners, builds a learner graph from validation-set
prediction agreement, solves the DSI integer program on that graph, and
compares the selected ensemble with natural same-size and full-ensemble
baselines.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
import shutil
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from benchmark_dsi_mip import (
    cbc_version,
    edge_list,
    graph_from_edges,
    selected_vertices,
    solve_with_cbc,
    write_linear_row,
    write_dsi_lp,
)
from ensemble_dsi_experiment import phi_correlation, percentile


DATASETS = {
    "iris": {
        "file": "iris.data",
        "source": "UCI Machine Learning Repository iris.data",
    },
    "penguins": {
        "file": "penguins.csv",
        "source": "Palmer Penguins penguins.csv",
    },
    "wine": {
        "file": "wine.data",
        "source": "UCI Machine Learning Repository wine.data",
    },
    "wdbc": {
        "file": "wdbc.data",
        "source": "UCI Machine Learning Repository wdbc.data",
    },
}


def read_csv_rows(path, has_header=False):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if has_header:
        return rows[0], rows[1:]
    return None, rows


def load_iris(path):
    _, rows = read_csv_rows(path)
    examples = []
    for row in rows:
        if not row:
            continue
        examples.append(([float(x) for x in row[:4]], row[4]))
    return examples, ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def load_wine(path):
    _, rows = read_csv_rows(path)
    examples = []
    for row in rows:
        if not row:
            continue
        examples.append(([float(x) for x in row[1:]], f"class_{row[0]}"))
    names = [f"feature_{i}" for i in range(1, 14)]
    return examples, names


def load_wdbc(path):
    _, rows = read_csv_rows(path)
    examples = []
    for row in rows:
        if not row:
            continue
        examples.append(([float(x) for x in row[2:]], row[1]))
    names = [f"feature_{i}" for i in range(1, 31)]
    return examples, names


def load_penguins(path):
    header, rows = read_csv_rows(path, has_header=True)
    index = {name: i for i, name in enumerate(header)}
    numeric = [
        "bill_length_mm",
        "bill_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "year",
    ]
    island_values = ["Biscoe", "Dream", "Torgersen"]
    sex_values = ["female", "male"]
    names = numeric + [f"island_{x}" for x in island_values] + [f"sex_{x}" for x in sex_values]
    examples = []
    for row in rows:
        species = row[index["species"]].strip()
        if not species:
            continue
        numeric_values = []
        missing = False
        for name in numeric:
            value = row[index[name]].strip()
            if value in ("", "NA", "."):
                missing = True
                break
            numeric_values.append(float(value))
        island = row[index["island"]].strip()
        sex = row[index["sex"]].strip().lower()
        if missing or island not in island_values or sex not in sex_values:
            continue
        features = numeric_values
        features += [1.0 if island == value else 0.0 for value in island_values]
        features += [1.0 if sex == value else 0.0 for value in sex_values]
        examples.append((features, species))
    return examples, names


def load_dataset(name, raw_dir):
    path = raw_dir / DATASETS[name]["file"]
    if not path.exists():
        raise FileNotFoundError(f"missing data file {path}")
    if name == "iris":
        return load_iris(path)
    if name == "penguins":
        return load_penguins(path)
    if name == "wine":
        return load_wine(path)
    if name == "wdbc":
        return load_wdbc(path)
    raise ValueError(f"unknown dataset {name}")


def split_by_class(examples, seed, train_fraction=0.60, validation_fraction=0.20):
    rng = random.Random(seed)
    by_label = defaultdict(list)
    for example in examples:
        by_label[example[1]].append(example)

    train = []
    validation = []
    test = []
    for label in sorted(by_label):
        items = list(by_label[label])
        rng.shuffle(items)
        n = len(items)
        n_train = max(1, int(round(train_fraction * n)))
        n_validation = max(1, int(round(validation_fraction * n)))
        if n_train + n_validation >= n:
            n_validation = max(1, n - n_train - 1)
        train.extend(items[:n_train])
        validation.extend(items[n_train : n_train + n_validation])
        test.extend(items[n_train + n_validation :])
    rng.shuffle(train)
    rng.shuffle(validation)
    rng.shuffle(test)
    return train, validation, test


def standardize(train, validation, test):
    feature_count = len(train[0][0])
    means = []
    scales = []
    for j in range(feature_count):
        values = [features[j] for features, _ in train]
        mean = statistics.mean(values)
        variance = statistics.mean((value - mean) ** 2 for value in values)
        scale = math.sqrt(variance) if variance > 1e-12 else 1.0
        means.append(mean)
        scales.append(scale)

    def transform(items):
        return [
            ([(features[j] - means[j]) / scales[j] for j in range(feature_count)], label)
            for features, label in items
        ]

    return transform(train), transform(validation), transform(test)


def label_order(items):
    return sorted({label for _, label in items})


def majority_label(labels):
    counts = Counter(labels)
    best_count = max(counts.values())
    return sorted(label for label, count in counts.items() if count == best_count)[0]


def euclidean_squared(a, b, features):
    return sum((a[j] - b[j]) ** 2 for j in features)


class NearestCentroid:
    def __init__(self, features):
        self.features = tuple(features)

    def fit(self, train):
        self.classes = label_order(train)
        self.centroids = {}
        for label in self.classes:
            rows = [features for features, y in train if y == label]
            self.centroids[label] = [
                statistics.mean(row[j] for row in rows) for j in range(len(train[0][0]))
            ]
        return self

    def predict_one(self, features):
        return min(
            self.classes,
            key=lambda label: (
                euclidean_squared(features, self.centroids[label], self.features),
                label,
            ),
        )


class KNearestNeighbors:
    def __init__(self, features, k):
        self.features = tuple(features)
        self.k = k

    def fit(self, train):
        self.train = list(train)
        self.classes = label_order(train)
        return self

    def predict_one(self, features):
        ranked = sorted(
            (
                euclidean_squared(features, train_features, self.features),
                label,
            )
            for train_features, label in self.train
        )
        votes = Counter(label for _, label in ranked[: self.k])
        best = max(votes.values())
        candidates = [label for label, count in votes.items() if count == best]
        if len(candidates) == 1:
            return candidates[0]
        distance_sum = {
            label: sum(distance for distance, y in ranked[: self.k] if y == label)
            for label in candidates
        }
        return min(candidates, key=lambda label: (distance_sum[label], label))


class GaussianNaiveBayes:
    def __init__(self, features):
        self.features = tuple(features)

    def fit(self, train):
        self.classes = label_order(train)
        self.priors = {}
        self.means = {}
        self.variances = {}
        n = len(train)
        for label in self.classes:
            rows = [features for features, y in train if y == label]
            self.priors[label] = len(rows) / n
            self.means[label] = {}
            self.variances[label] = {}
            for j in self.features:
                values = [row[j] for row in rows]
                mean = statistics.mean(values)
                variance = statistics.mean((value - mean) ** 2 for value in values)
                self.means[label][j] = mean
                self.variances[label][j] = max(variance, 1e-6)
        return self

    def predict_one(self, features):
        scores = {}
        for label in self.classes:
            score = math.log(self.priors[label])
            for j in self.features:
                variance = self.variances[label][j]
                delta = features[j] - self.means[label][j]
                score += -0.5 * math.log(2 * math.pi * variance)
                score += -(delta * delta) / (2 * variance)
            scores[label] = score
        return max(self.classes, key=lambda label: (scores[label], label))


class DecisionStump:
    def __init__(self, features):
        self.features = tuple(features)

    def fit(self, train):
        self.default_label = majority_label([label for _, label in train])
        best_error = len(train) + 1
        best_rule = None
        for j in self.features:
            values = sorted({features[j] for features, _ in train})
            if len(values) == 1:
                thresholds = values
            else:
                thresholds = [(values[i] + values[i + 1]) / 2 for i in range(len(values) - 1)]
            for threshold in thresholds:
                left = [label for features, label in train if features[j] <= threshold]
                right = [label for features, label in train if features[j] > threshold]
                if not left or not right:
                    continue
                left_label = majority_label(left)
                right_label = majority_label(right)
                error = sum(
                    (left_label if features[j] <= threshold else right_label) != label
                    for features, label in train
                )
                if error < best_error:
                    best_error = error
                    best_rule = (j, threshold, left_label, right_label)
        self.rule = best_rule
        return self

    def predict_one(self, features):
        if self.rule is None:
            return self.default_label
        j, threshold, left_label, right_label = self.rule
        return left_label if features[j] <= threshold else right_label


def predict_many(model, items):
    return [model.predict_one(features) for features, _ in items]


def accuracy(labels, predictions):
    return sum(y == yhat for y, yhat in zip(labels, predictions)) / len(labels)


def feature_subset(rng, feature_count, mode):
    if mode == "all":
        return tuple(range(feature_count))
    if mode == "sqrt":
        size = max(1, int(round(math.sqrt(feature_count))))
    elif mode == "third":
        size = max(1, int(round(feature_count / 3)))
    elif mode == "half":
        size = max(1, int(round(feature_count / 2)))
    else:
        size = 1
    return tuple(sorted(rng.sample(range(feature_count), min(size, feature_count))))


def make_learner_specs(feature_count, seed, target_count):
    rng = random.Random(seed)
    specs = []

    def add(kind, features, k=None):
        name = kind
        if k is not None:
            name += f"_k{k}"
        name += "_" + "-".join(str(j) for j in features)
        specs.append((kind, tuple(features), k, name))

    all_features = tuple(range(feature_count))
    for kind in ("centroid", "gnb"):
        add(kind, all_features)
    for k in (1, 3, 5, 7, 9):
        add("knn", all_features, k)
    for j in range(feature_count):
        add("stump", (j,))

    modes = ["sqrt", "third", "half", "one"]
    kinds = ["centroid", "gnb", "knn", "stump"]
    seen = {spec[3] for spec in specs}
    attempts = 0
    while len(specs) < target_count and attempts < 5000:
        attempts += 1
        kind = rng.choice(kinds)
        mode = rng.choice(modes)
        features = feature_subset(rng, feature_count, mode)
        k = rng.choice((1, 3, 5, 7, 9)) if kind == "knn" else None
        name = kind
        if k is not None:
            name += f"_k{k}"
        name += "_" + "-".join(str(j) for j in features)
        if name in seen:
            continue
        seen.add(name)
        specs.append((kind, features, k, name))
    return specs[:target_count]


def build_model(kind, features, k):
    if kind == "centroid":
        return NearestCentroid(features)
    if kind == "gnb":
        return GaussianNaiveBayes(features)
    if kind == "knn":
        return KNearestNeighbors(features, k)
    if kind == "stump":
        return DecisionStump(features)
    raise ValueError(f"unknown learner kind {kind}")


def train_pool(train, validation, test, seed, target_count):
    feature_count = len(train[0][0])
    specs = make_learner_specs(feature_count, seed, target_count)
    validation_labels = [label for _, label in validation]
    test_labels = [label for _, label in test]
    learners = []
    for index, (kind, features, k, name) in enumerate(specs):
        model = build_model(kind, features, k).fit(train)
        validation_predictions = predict_many(model, validation)
        test_predictions = predict_many(model, test)
        learners.append(
            {
                "index": index,
                "name": name,
                "kind": kind,
                "features": features,
                "validation_predictions": validation_predictions,
                "test_predictions": test_predictions,
                "validation_accuracy": accuracy(validation_labels, validation_predictions),
                "test_accuracy": accuracy(test_labels, test_predictions),
            }
        )
    return learners


def validation_competent_candidates(learners, slack, minimum):
    best = max(learner["validation_accuracy"] for learner in learners)
    cutoff = best - slack
    candidates = [i for i, learner in enumerate(learners) if learner["validation_accuracy"] >= cutoff]
    if len(candidates) < minimum:
        candidates = sorted(
            range(len(learners)),
            key=lambda i: (-learners[i]["validation_accuracy"], i),
        )[: min(minimum, len(learners))]
    filtered = []
    for local_index, original_index in enumerate(candidates):
        learner = dict(learners[original_index])
        learner["original_index"] = original_index
        learner["index"] = local_index
        filtered.append(learner)
    return filtered, cutoff


def agreement(a, b):
    return sum(x == y for x, y in zip(a, b)) / len(a)


def build_agreement_graph(learners, density):
    pair_scores = []
    for i, j in itertools.combinations(range(len(learners)), 2):
        score = agreement(
            learners[i]["validation_predictions"],
            learners[j]["validation_predictions"],
        )
        pair_scores.append((score, i, j))

    edge_count = max(1, int(round(density * len(pair_scores))))
    pair_scores.sort(reverse=True)
    threshold = pair_scores[edge_count - 1][0]
    edges = [(i, j) for score, i, j in pair_scores if score >= threshold]
    adj = graph_from_edges(len(learners), edges)
    return adj, threshold, pair_scores


def solve_dsi_partition(adj, out_dir, trial_name, cbc_cmd, time_limit):
    lp_dir = out_dir / "lp"
    log_dir = out_dir / "logs"
    sol_dir = out_dir / "solutions"
    for directory in (lp_dir, log_dir, sol_dir):
        directory.mkdir(parents=True, exist_ok=True)

    lp_path = lp_dir / f"{trial_name}.lp"
    log_path = log_dir / f"{trial_name}.log"
    sol_path = sol_dir / f"{trial_name}.sol"
    write_dsi_lp(adj, lp_path)
    status, objective, values, parsed_log, elapsed = solve_with_cbc(
        lp_path, sol_path, log_path, cbc_cmd, time_limit
    )
    n = len(adj)
    red = [int(v) for v in selected_vertices(values, "r", n)]
    blue = [int(v) for v in selected_vertices(values, "b", n)]
    return {
        "status": status,
        "objective": int(round(objective)) if objective != "" else "",
        "red": red,
        "blue": blue,
        "elapsed": elapsed,
        "cbc_wall_time": parsed_log["cbc_wall_time"],
        "cbc_nodes": parsed_log["cbc_nodes"],
        "lp_file": str(lp_path.relative_to(out_dir)),
        "log_file": str(log_path.relative_to(out_dir)),
        "solution_file": str(sol_path.relative_to(out_dir)),
    }


def write_lexicographic_dsi_lp(adj, weights, target_size, path):
    n = len(adj)
    edges = edge_list(adj)
    r = [f"r_{v}" for v in range(n)]
    b = [f"b_{v}" for v in range(n)]
    weighted_terms = [f"{weights[v]:.6f} {r[v]}" for v in range(n)]
    weighted_terms += [f"{weights[v]:.6f} {b[v]}" for v in range(n)]

    with path.open("w", encoding="utf-8") as f:
        f.write("Maximize\n")
        write_linear_row(f, "obj", weighted_terms)
        f.write("Subject To\n")
        write_linear_row(f, "red_nonempty", r, ">=", 1)
        write_linear_row(f, "blue_nonempty", b, ">=", 1)
        write_linear_row(f, "size_ge", r + b, ">=", target_size)
        write_linear_row(f, "size_le", r + b, "<=", target_size)

        for v in range(n):
            f.write(f" disjoint_{v}: {r[v]} + {b[v]} <= 1\n")

        for i, (u, v) in enumerate(edges):
            f.write(f" red_ind_{i}: {r[u]} + {r[v]} <= 1\n")
            f.write(f" blue_ind_{i}: {b[u]} + {b[v]} <= 1\n")

        for v in range(n):
            red_terms = [r[u] for u in sorted(adj[v])] + [r[v], b[v]]
            blue_terms = [b[u] for u in sorted(adj[v])] + [r[v], b[v]]
            write_linear_row(f, f"red_dom_{v}", red_terms, ">=", 1)
            write_linear_row(f, f"blue_dom_{v}", blue_terms, ">=", 1)

        f.write("Binary\n")
        for var in r + b:
            f.write(f" {var}\n")
        f.write("End\n")


def solve_lexicographic_dsi_partition(adj, weights, target_size, out_dir, trial_name, cbc_cmd, time_limit):
    lp_dir = out_dir / "lp"
    log_dir = out_dir / "logs"
    sol_dir = out_dir / "solutions"
    for directory in (lp_dir, log_dir, sol_dir):
        directory.mkdir(parents=True, exist_ok=True)

    lp_path = lp_dir / f"{trial_name}.lp"
    log_path = log_dir / f"{trial_name}.log"
    sol_path = sol_dir / f"{trial_name}.sol"
    write_lexicographic_dsi_lp(adj, weights, target_size, lp_path)
    status, objective, values, parsed_log, elapsed = solve_with_cbc(
        lp_path, sol_path, log_path, cbc_cmd, time_limit
    )
    n = len(adj)
    red = [int(v) for v in selected_vertices(values, "r", n)]
    blue = [int(v) for v in selected_vertices(values, "b", n)]
    return {
        "status": status,
        "objective": objective,
        "red": red,
        "blue": blue,
        "elapsed": elapsed,
        "cbc_wall_time": parsed_log["cbc_wall_time"],
        "cbc_nodes": parsed_log["cbc_nodes"],
        "lp_file": str(lp_path.relative_to(out_dir)),
        "log_file": str(log_path.relative_to(out_dir)),
        "solution_file": str(sol_path.relative_to(out_dir)),
    }


def ensemble_predictions(learners, selected, split, tie_order):
    predictions = []
    for sample_index in range(len(learners[0][f"{split}_predictions"])):
        votes = Counter(learners[i][f"{split}_predictions"][sample_index] for i in selected)
        best = max(votes.values())
        candidates = {label for label, count in votes.items() if count == best}
        if len(candidates) == 1:
            predictions.append(next(iter(candidates)))
            continue
        for learner_index in tie_order:
            label = learners[learner_index][f"{split}_predictions"][sample_index]
            if label in candidates:
                predictions.append(label)
                break
    return predictions


def ensemble_accuracy(learners, labels, selected, split):
    tie_order = sorted(selected, key=lambda i: (-learners[i]["validation_accuracy"], i))
    predictions = ensemble_predictions(learners, selected, split, tie_order)
    return accuracy(labels, predictions)


def mean_pair_agreement(learners, selected, split):
    pairs = list(itertools.combinations(selected, 2))
    if not pairs:
        return 1.0
    key = f"{split}_predictions"
    return statistics.mean(agreement(learners[i][key], learners[j][key]) for i, j in pairs)


def mean_error_correlation(learners, labels, selected, split):
    pairs = list(itertools.combinations(selected, 2))
    if not pairs:
        return 0.0
    key = f"{split}_predictions"
    errors = [
        [1 if prediction != label else 0 for prediction, label in zip(learner[key], labels)]
        for learner in learners
    ]
    return statistics.mean(phi_correlation(errors[i], errors[j]) for i, j in pairs)


def clean_output_dirs(out_dir):
    for subdir, pattern in (("lp", "*.lp"), ("logs", "*.log"), ("solutions", "*.sol")):
        directory = out_dir / subdir
        directory.mkdir(parents=True, exist_ok=True)
        for old_file in directory.glob(pattern):
            old_file.unlink()


def write_csv(rows, path, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def signed_token(coefficient, variable, first):
    magnitude = abs(coefficient)
    if abs(magnitude - 1.0) < 1e-12:
        body = variable
    else:
        body = f"{magnitude:.6f} {variable}"
    if first:
        return f"- {body}" if coefficient < 0 else body
    return f"- {body}" if coefficient < 0 else f"+ {body}"


def write_signed_row(f, name, terms, sense, rhs, width=90):
    terms = [(coefficient, variable) for coefficient, variable in terms if abs(coefficient) > 1e-12]
    if not terms:
        terms = [(1.0, "0")]
    line = f" {name}:"
    first = True
    for coefficient, variable in terms:
        token = signed_token(coefficient, variable, first)
        piece = f" {token}"
        if len(line) + len(piece) > width and line.strip() != f"{name}:":
            f.write(line + "\n")
            line = f"  {token}"
        else:
            line += piece
        first = False
    tail = f" {sense} {rhs}"
    if len(line) + len(tail) > width:
        f.write(line + "\n")
        line = f"  {tail.strip()}"
    else:
        line += tail
    f.write(line + "\n")


def write_validation_margin_dsi_lp(
    adj,
    learners,
    validation_labels,
    target_size,
    path,
    accuracy_tiebreak=0.001,
):
    n = len(adj)
    edges = edge_list(adj)
    r = [f"r_{v}" for v in range(n)]
    b = [f"b_{v}" for v in range(n)]
    c = [f"c_{t}" for t in range(len(validation_labels))]
    labels = sorted(set(validation_labels))
    weights = [accuracy_tiebreak * learner["validation_accuracy"] for learner in learners]
    objective_terms = list(c)
    objective_terms += [f"{weights[v]:.6f} {r[v]}" for v in range(n)]
    objective_terms += [f"{weights[v]:.6f} {b[v]}" for v in range(n)]
    margin_constant = target_size + 1

    with path.open("w", encoding="utf-8") as f:
        f.write("Maximize\n")
        write_linear_row(f, "obj", objective_terms)
        f.write("Subject To\n")
        write_linear_row(f, "red_nonempty", r, ">=", 1)
        write_linear_row(f, "blue_nonempty", b, ">=", 1)
        write_linear_row(f, "size_ge", r + b, ">=", target_size)
        write_linear_row(f, "size_le", r + b, "<=", target_size)

        for v in range(n):
            f.write(f" disjoint_{v}: {r[v]} + {b[v]} <= 1\n")

        for i, (u, v) in enumerate(edges):
            f.write(f" red_ind_{i}: {r[u]} + {r[v]} <= 1\n")
            f.write(f" blue_ind_{i}: {b[u]} + {b[v]} <= 1\n")

        for v in range(n):
            red_terms = [r[u] for u in sorted(adj[v])] + [r[v], b[v]]
            blue_terms = [b[u] for u in sorted(adj[v])] + [r[v], b[v]]
            write_linear_row(f, f"red_dom_{v}", red_terms, ">=", 1)
            write_linear_row(f, f"blue_dom_{v}", blue_terms, ">=", 1)

        for t, true_label in enumerate(validation_labels):
            for label_index, other_label in enumerate(label for label in labels if label != true_label):
                terms = [(margin_constant, c[t])]
                for v, learner in enumerate(learners):
                    prediction = learner["validation_predictions"][t]
                    if prediction == other_label:
                        terms.append((1.0, r[v]))
                        terms.append((1.0, b[v]))
                    elif prediction == true_label:
                        terms.append((-1.0, r[v]))
                        terms.append((-1.0, b[v]))
                write_signed_row(
                    f,
                    f"margin_{t}_{label_index}",
                    terms,
                    "<=",
                    margin_constant - 1,
                )

        f.write("Binary\n")
        for var in r + b + c:
            f.write(f" {var}\n")
        f.write("End\n")


def solve_validation_margin_dsi_partition(
    adj,
    learners,
    validation_labels,
    target_size,
    out_dir,
    trial_name,
    cbc_cmd,
    time_limit,
):
    lp_dir = out_dir / "lp"
    log_dir = out_dir / "logs"
    sol_dir = out_dir / "solutions"
    for directory in (lp_dir, log_dir, sol_dir):
        directory.mkdir(parents=True, exist_ok=True)

    lp_path = lp_dir / f"{trial_name}.lp"
    log_path = log_dir / f"{trial_name}.log"
    sol_path = sol_dir / f"{trial_name}.sol"
    write_validation_margin_dsi_lp(adj, learners, validation_labels, target_size, lp_path)
    status, objective, values, parsed_log, elapsed = solve_with_cbc(
        lp_path, sol_path, log_path, cbc_cmd, time_limit
    )
    n = len(adj)
    red = [int(v) for v in selected_vertices(values, "r", n)]
    blue = [int(v) for v in selected_vertices(values, "b", n)]
    correct_margin = sum(1 for name, value in values.items() if name.startswith("c_") and value > 0.5)
    return {
        "status": status,
        "objective": objective,
        "validation_margin_correct": correct_margin,
        "red": red,
        "blue": blue,
        "elapsed": elapsed,
        "cbc_wall_time": parsed_log["cbc_wall_time"],
        "cbc_nodes": parsed_log["cbc_nodes"],
        "lp_file": str(lp_path.relative_to(out_dir)),
        "log_file": str(log_path.relative_to(out_dir)),
        "solution_file": str(sol_path.relative_to(out_dir)),
    }


def run_trial(dataset, examples, feature_names, trial, args, out_dir):
    train, validation, test = split_by_class(examples, args.seed + 1000 * trial)
    train, validation, test = standardize(train, validation, test)
    base_learners = train_pool(train, validation, test, args.seed + 5000 * trial, args.learners)
    learners, validation_cutoff = validation_competent_candidates(
        base_learners,
        args.validation_slack,
        args.min_candidates,
    )
    validation_labels = [label for _, label in validation]
    test_labels = [label for _, label in test]

    adj, threshold, pair_scores = build_agreement_graph(learners, args.edge_density)
    trial_name = f"{dataset}_trial_{trial:03d}"
    dsi = solve_dsi_partition(adj, out_dir, trial_name, args.cbc, args.time_limit)
    selected = dsi["red"] + dsi["blue"]
    selected_size = len(selected)
    validation_weights = [learner["validation_accuracy"] for learner in learners]
    lex_dsi = solve_lexicographic_dsi_partition(
        adj,
        validation_weights,
        selected_size,
        out_dir,
        f"{trial_name}_lex",
        args.cbc,
        args.time_limit,
    )
    lex_selected = lex_dsi["red"] + lex_dsi["blue"]
    margin_dsi = solve_validation_margin_dsi_partition(
        adj,
        learners,
        validation_labels,
        selected_size,
        out_dir,
        f"{trial_name}_margin",
        args.cbc,
        args.time_limit,
    )
    margin_selected = margin_dsi["red"] + margin_dsi["blue"]

    topk = sorted(range(len(learners)), key=lambda i: (-learners[i]["validation_accuracy"], i))[
        :selected_size
    ]
    full = list(range(len(learners)))
    best_index = topk[0]

    rng = random.Random(args.seed + 9000 * trial)
    random_accuracies = []
    random_agreements = []
    random_error_correlations = []
    for _ in range(args.random_samples):
        sample = rng.sample(range(len(learners)), selected_size)
        random_accuracies.append(ensemble_accuracy(learners, test_labels, sample, "test"))
        random_agreements.append(mean_pair_agreement(learners, sample, "test"))
        random_error_correlations.append(mean_error_correlation(learners, test_labels, sample, "test"))

    dsi_test_accuracy = ensemble_accuracy(learners, test_labels, selected, "test")
    lex_dsi_test_accuracy = ensemble_accuracy(learners, test_labels, lex_selected, "test")
    margin_dsi_test_accuracy = ensemble_accuracy(learners, test_labels, margin_selected, "test")
    topk_test_accuracy = ensemble_accuracy(learners, test_labels, topk, "test")
    full_test_accuracy = ensemble_accuracy(learners, test_labels, full, "test")
    dsi_validation_accuracy = ensemble_accuracy(learners, validation_labels, selected, "validation")
    lex_dsi_validation_accuracy = ensemble_accuracy(
        learners,
        validation_labels,
        lex_selected,
        "validation",
    )
    margin_dsi_validation_accuracy = ensemble_accuracy(
        learners,
        validation_labels,
        margin_selected,
        "validation",
    )
    topk_validation_accuracy = ensemble_accuracy(learners, validation_labels, topk, "validation")

    graph_edges = sum(len(nbrs) for nbrs in adj) // 2
    possible_edges = len(learners) * (len(learners) - 1) / 2
    agreements = [score for score, _, _ in pair_scores]

    return {
        "dataset": dataset,
        "trial": trial,
        "examples": len(examples),
        "features": len(feature_names),
        "classes": len(label_order(examples)),
        "train_size": len(train),
        "validation_size": len(validation),
        "test_size": len(test),
        "base_learners": len(base_learners),
        "candidate_learners": len(learners),
        "validation_slack": f"{args.validation_slack:.3f}",
        "validation_accuracy_cutoff": f"{validation_cutoff:.6f}",
        "edge_density_target": f"{args.edge_density:.3f}",
        "edge_threshold": f"{threshold:.6f}",
        "graph_edges": graph_edges,
        "graph_density": f"{graph_edges / possible_edges:.6f}",
        "mean_pair_validation_agreement": f"{statistics.mean(agreements):.6f}",
        "gamma_dsi": dsi["objective"],
        "red_size": len(dsi["red"]),
        "blue_size": len(dsi["blue"]),
        "selected_size": selected_size,
        "red_vertices": " ".join(str(v) for v in dsi["red"]),
        "blue_vertices": " ".join(str(v) for v in dsi["blue"]),
        "lex_red_size": len(lex_dsi["red"]),
        "lex_blue_size": len(lex_dsi["blue"]),
        "lex_red_vertices": " ".join(str(v) for v in lex_dsi["red"]),
        "lex_blue_vertices": " ".join(str(v) for v in lex_dsi["blue"]),
        "lex_dsi_weight_objective": f"{float(lex_dsi['objective']):.6f}",
        "lex_dsi_changed_selection": int(set(lex_selected) != set(selected)),
        "margin_red_size": len(margin_dsi["red"]),
        "margin_blue_size": len(margin_dsi["blue"]),
        "margin_red_vertices": " ".join(str(v) for v in margin_dsi["red"]),
        "margin_blue_vertices": " ".join(str(v) for v in margin_dsi["blue"]),
        "margin_dsi_weight_objective": f"{float(margin_dsi['objective']):.6f}",
        "margin_dsi_validation_strict_correct": margin_dsi["validation_margin_correct"],
        "margin_dsi_changed_selection": int(set(margin_selected) != set(selected)),
        "dsi_validation_accuracy": f"{dsi_validation_accuracy:.6f}",
        "lex_dsi_validation_accuracy": f"{lex_dsi_validation_accuracy:.6f}",
        "margin_dsi_validation_accuracy": f"{margin_dsi_validation_accuracy:.6f}",
        "topk_validation_accuracy": f"{topk_validation_accuracy:.6f}",
        "dsi_test_accuracy": f"{dsi_test_accuracy:.6f}",
        "lex_dsi_test_accuracy": f"{lex_dsi_test_accuracy:.6f}",
        "margin_dsi_test_accuracy": f"{margin_dsi_test_accuracy:.6f}",
        "topk_test_accuracy": f"{topk_test_accuracy:.6f}",
        "full_test_accuracy": f"{full_test_accuracy:.6f}",
        "best_individual_test_accuracy": f"{learners[best_index]['test_accuracy']:.6f}",
        "random_mean_test_accuracy": f"{statistics.mean(random_accuracies):.6f}",
        "random_sd_test_accuracy": f"{statistics.stdev(random_accuracies):.6f}",
        "dsi_minus_random_accuracy": f"{dsi_test_accuracy - statistics.mean(random_accuracies):.6f}",
        "lex_dsi_minus_random_accuracy": f"{lex_dsi_test_accuracy - statistics.mean(random_accuracies):.6f}",
        "margin_dsi_minus_random_accuracy": f"{margin_dsi_test_accuracy - statistics.mean(random_accuracies):.6f}",
        "dsi_minus_topk_accuracy": f"{dsi_test_accuracy - topk_test_accuracy:.6f}",
        "lex_dsi_minus_topk_accuracy": f"{lex_dsi_test_accuracy - topk_test_accuracy:.6f}",
        "margin_dsi_minus_topk_accuracy": f"{margin_dsi_test_accuracy - topk_test_accuracy:.6f}",
        "dsi_minus_full_accuracy": f"{dsi_test_accuracy - full_test_accuracy:.6f}",
        "lex_dsi_minus_full_accuracy": f"{lex_dsi_test_accuracy - full_test_accuracy:.6f}",
        "margin_dsi_minus_full_accuracy": f"{margin_dsi_test_accuracy - full_test_accuracy:.6f}",
        "dsi_accuracy_percentile": f"{percentile(dsi_test_accuracy, random_accuracies):.6f}",
        "lex_dsi_accuracy_percentile": f"{percentile(lex_dsi_test_accuracy, random_accuracies):.6f}",
        "margin_dsi_accuracy_percentile": f"{percentile(margin_dsi_test_accuracy, random_accuracies):.6f}",
        "dsi_mean_pair_agreement": f"{mean_pair_agreement(learners, selected, 'test'):.6f}",
        "lex_dsi_mean_pair_agreement": f"{mean_pair_agreement(learners, lex_selected, 'test'):.6f}",
        "margin_dsi_mean_pair_agreement": f"{mean_pair_agreement(learners, margin_selected, 'test'):.6f}",
        "topk_mean_pair_agreement": f"{mean_pair_agreement(learners, topk, 'test'):.6f}",
        "random_mean_pair_agreement": f"{statistics.mean(random_agreements):.6f}",
        "dsi_avg_error_correlation": f"{mean_error_correlation(learners, test_labels, selected, 'test'):.6f}",
        "lex_dsi_avg_error_correlation": f"{mean_error_correlation(learners, test_labels, lex_selected, 'test'):.6f}",
        "margin_dsi_avg_error_correlation": f"{mean_error_correlation(learners, test_labels, margin_selected, 'test'):.6f}",
        "topk_avg_error_correlation": f"{mean_error_correlation(learners, test_labels, topk, 'test'):.6f}",
        "random_mean_error_correlation": f"{statistics.mean(random_error_correlations):.6f}",
        "dsi_status": dsi["status"],
        "lex_dsi_status": lex_dsi["status"],
        "margin_dsi_status": margin_dsi["status"],
        "cbc_wall_time_seconds": dsi["cbc_wall_time"],
        "lex_cbc_wall_time_seconds": lex_dsi["cbc_wall_time"],
        "margin_cbc_wall_time_seconds": margin_dsi["cbc_wall_time"],
        "driver_wall_time_seconds": f"{dsi['elapsed']:.6f}",
        "lex_driver_wall_time_seconds": f"{lex_dsi['elapsed']:.6f}",
        "margin_driver_wall_time_seconds": f"{margin_dsi['elapsed']:.6f}",
        "cbc_nodes": dsi["cbc_nodes"],
        "lex_cbc_nodes": lex_dsi["cbc_nodes"],
        "margin_cbc_nodes": margin_dsi["cbc_nodes"],
        "lp_file": dsi["lp_file"],
        "log_file": dsi["log_file"],
        "solution_file": dsi["solution_file"],
        "lex_lp_file": lex_dsi["lp_file"],
        "lex_log_file": lex_dsi["log_file"],
        "lex_solution_file": lex_dsi["solution_file"],
        "margin_lp_file": margin_dsi["lp_file"],
        "margin_log_file": margin_dsi["log_file"],
        "margin_solution_file": margin_dsi["solution_file"],
    }


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["dataset"]].append(row)

    def numeric(group, key):
        return [float(row[key]) for row in group]

    summary = []
    for dataset in sorted(groups):
        group = groups[dataset]
        dsi_minus_random = numeric(group, "dsi_minus_random_accuracy")
        lex_dsi_minus_random = numeric(group, "lex_dsi_minus_random_accuracy")
        margin_dsi_minus_random = numeric(group, "margin_dsi_minus_random_accuracy")
        dsi_minus_topk = numeric(group, "dsi_minus_topk_accuracy")
        lex_dsi_minus_topk = numeric(group, "lex_dsi_minus_topk_accuracy")
        margin_dsi_minus_topk = numeric(group, "margin_dsi_minus_topk_accuracy")
        dsi_minus_full = numeric(group, "dsi_minus_full_accuracy")
        lex_dsi_minus_full = numeric(group, "lex_dsi_minus_full_accuracy")
        margin_dsi_minus_full = numeric(group, "margin_dsi_minus_full_accuracy")
        summary.append(
            {
                "dataset": dataset,
                "trials": len(group),
                "examples": group[0]["examples"],
                "features": group[0]["features"],
                "classes": group[0]["classes"],
                "base_learners": group[0]["base_learners"],
                "candidate_learners": f"{statistics.mean(numeric(group, 'candidate_learners')):.3f}",
                "mean_graph_density": f"{statistics.mean(numeric(group, 'graph_density')):.6f}",
                "mean_edge_threshold": f"{statistics.mean(numeric(group, 'edge_threshold')):.6f}",
                "optimal_dsi_trials": sum(row["dsi_status"] == "Optimal" for row in group),
                "optimal_lex_dsi_trials": sum(row["lex_dsi_status"] == "Optimal" for row in group),
                "optimal_margin_dsi_trials": sum(row["margin_dsi_status"] == "Optimal" for row in group),
                "mean_gamma_dsi": f"{statistics.mean(numeric(group, 'gamma_dsi')):.3f}",
                "mean_selected_fraction": f"{statistics.mean(numeric(group, 'selected_size')) / statistics.mean(numeric(group, 'candidate_learners')):.6f}",
                "lex_dsi_changed_selections": sum(int(row["lex_dsi_changed_selection"]) for row in group),
                "margin_dsi_changed_selections": sum(int(row["margin_dsi_changed_selection"]) for row in group),
                "mean_dsi_accuracy": f"{statistics.mean(numeric(group, 'dsi_test_accuracy')):.6f}",
                "mean_lex_dsi_accuracy": f"{statistics.mean(numeric(group, 'lex_dsi_test_accuracy')):.6f}",
                "mean_margin_dsi_accuracy": f"{statistics.mean(numeric(group, 'margin_dsi_test_accuracy')):.6f}",
                "mean_topk_accuracy": f"{statistics.mean(numeric(group, 'topk_test_accuracy')):.6f}",
                "mean_full_accuracy": f"{statistics.mean(numeric(group, 'full_test_accuracy')):.6f}",
                "mean_best_individual_accuracy": f"{statistics.mean(numeric(group, 'best_individual_test_accuracy')):.6f}",
                "mean_random_accuracy": f"{statistics.mean(numeric(group, 'random_mean_test_accuracy')):.6f}",
                "mean_dsi_minus_random": f"{statistics.mean(dsi_minus_random):.6f}",
                "mean_lex_dsi_minus_random": f"{statistics.mean(lex_dsi_minus_random):.6f}",
                "mean_margin_dsi_minus_random": f"{statistics.mean(margin_dsi_minus_random):.6f}",
                "mean_dsi_minus_topk": f"{statistics.mean(dsi_minus_topk):.6f}",
                "mean_lex_dsi_minus_topk": f"{statistics.mean(lex_dsi_minus_topk):.6f}",
                "mean_margin_dsi_minus_topk": f"{statistics.mean(margin_dsi_minus_topk):.6f}",
                "mean_dsi_minus_full": f"{statistics.mean(dsi_minus_full):.6f}",
                "mean_lex_dsi_minus_full": f"{statistics.mean(lex_dsi_minus_full):.6f}",
                "mean_margin_dsi_minus_full": f"{statistics.mean(margin_dsi_minus_full):.6f}",
                "dsi_wins_vs_random_mean": sum(value > 0 for value in dsi_minus_random),
                "lex_dsi_wins_vs_random_mean": sum(value > 0 for value in lex_dsi_minus_random),
                "margin_dsi_wins_vs_random_mean": sum(value > 0 for value in margin_dsi_minus_random),
                "dsi_wins_vs_topk": sum(value > 0 for value in dsi_minus_topk),
                "lex_dsi_wins_vs_topk": sum(value > 0 for value in lex_dsi_minus_topk),
                "margin_dsi_wins_vs_topk": sum(value > 0 for value in margin_dsi_minus_topk),
                "dsi_wins_vs_full": sum(value > 0 for value in dsi_minus_full),
                "lex_dsi_wins_vs_full": sum(value > 0 for value in lex_dsi_minus_full),
                "margin_dsi_wins_vs_full": sum(value > 0 for value in margin_dsi_minus_full),
                "mean_dsi_percentile_vs_random": f"{statistics.mean(numeric(group, 'dsi_accuracy_percentile')):.6f}",
                "mean_lex_dsi_percentile_vs_random": f"{statistics.mean(numeric(group, 'lex_dsi_accuracy_percentile')):.6f}",
                "mean_margin_dsi_percentile_vs_random": f"{statistics.mean(numeric(group, 'margin_dsi_accuracy_percentile')):.6f}",
                "mean_dsi_pair_agreement": f"{statistics.mean(numeric(group, 'dsi_mean_pair_agreement')):.6f}",
                "mean_lex_dsi_pair_agreement": f"{statistics.mean(numeric(group, 'lex_dsi_mean_pair_agreement')):.6f}",
                "mean_margin_dsi_pair_agreement": f"{statistics.mean(numeric(group, 'margin_dsi_mean_pair_agreement')):.6f}",
                "mean_topk_pair_agreement": f"{statistics.mean(numeric(group, 'topk_mean_pair_agreement')):.6f}",
                "mean_random_pair_agreement": f"{statistics.mean(numeric(group, 'random_mean_pair_agreement')):.6f}",
                "mean_dsi_error_correlation": f"{statistics.mean(numeric(group, 'dsi_avg_error_correlation')):.6f}",
                "mean_lex_dsi_error_correlation": f"{statistics.mean(numeric(group, 'lex_dsi_avg_error_correlation')):.6f}",
                "mean_margin_dsi_error_correlation": f"{statistics.mean(numeric(group, 'margin_dsi_avg_error_correlation')):.6f}",
                "mean_topk_error_correlation": f"{statistics.mean(numeric(group, 'topk_avg_error_correlation')):.6f}",
                "mean_random_error_correlation": f"{statistics.mean(numeric(group, 'random_mean_error_correlation')):.6f}",
                "mean_driver_wall_time_seconds": f"{statistics.mean(numeric(group, 'driver_wall_time_seconds')):.6f}",
                "mean_lex_driver_wall_time_seconds": f"{statistics.mean(numeric(group, 'lex_driver_wall_time_seconds')):.6f}",
                "mean_margin_driver_wall_time_seconds": f"{statistics.mean(numeric(group, 'margin_driver_wall_time_seconds')):.6f}",
                "max_driver_wall_time_seconds": f"{max(numeric(group, 'driver_wall_time_seconds')):.6f}",
                "max_lex_driver_wall_time_seconds": f"{max(numeric(group, 'lex_driver_wall_time_seconds')):.6f}",
                "max_margin_driver_wall_time_seconds": f"{max(numeric(group, 'margin_driver_wall_time_seconds')):.6f}",
            }
        )
    return summary


def write_metadata(out_dir, args, row_count):
    lines = [
        "Real-data DSI ensemble experiment metadata",
        "==========================================",
        f"Datasets: {', '.join(args.datasets)}",
        f"Trials per dataset: {args.trials}",
        f"Base learners per trial: {args.learners}",
        f"Validation-accuracy slack for candidate filtering: {args.validation_slack}",
        f"Minimum candidate learners after filtering: {args.min_candidates}",
        f"Target validation-agreement graph density: {args.edge_density}",
        f"Random same-size ensembles per trial: {args.random_samples}",
        "Lexicographic refinement: first minimize DSI size, then maximize",
        "the sum of selected individual validation accuracies among DSI sets",
        "of that minimum size.",
        "Validation-margin refinement: first minimize DSI size, then maximize",
        "the number of validation examples on which the correct class receives",
        "a strict plurality vote among selected learners, with individual",
        "validation accuracy used only as a small tie-breaker.",
        f"CBC time limit per DSI solve: {args.time_limit}",
        f"CBC command: {args.cbc}",
        f"CBC version: {cbc_version(args.cbc)}",
        f"Python: {sys.version.split()[0]}",
        "",
        "Dataset sources:",
    ]
    for name in args.datasets:
        lines.append(f"- {name}: {DATASETS[name]['source']}")
    lines += [
        "",
        "Rerun from the teresa-dom directory with:",
        "python3 computational_data/real_data_dsi_experiment.py",
        "",
        f"Rows written: {row_count}",
        "",
    ]
    (out_dir / "metadata.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="computational_data/real_data")
    parser.add_argument("--raw-dir", default="computational_data/real_data/raw")
    parser.add_argument("--cbc", default=shutil.which("cbc") or "cbc")
    parser.add_argument("--time-limit", type=float, default=10.0)
    parser.add_argument("--datasets", nargs="+", default=["iris", "penguins", "wine", "wdbc"])
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--learners", type=int, default=48)
    parser.add_argument("--validation-slack", type=float, default=0.05)
    parser.add_argument("--min-candidates", type=int, default=16)
    parser.add_argument("--edge-density", type=float, default=0.25)
    parser.add_argument("--random-samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260519)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    raw_dir = Path(args.raw_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    clean_output_dirs(out_dir)

    rows = []
    for dataset in args.datasets:
        examples, feature_names = load_dataset(dataset, raw_dir)
        for trial in range(args.trials):
            rows.append(run_trial(dataset, examples, feature_names, trial, args, out_dir))

    trial_path = out_dir / "real_data_dsi_trials.csv"
    summary_path = out_dir / "real_data_dsi_summary.csv"
    write_csv(rows, trial_path, list(rows[0].keys()))
    summary = summarize(rows)
    write_csv(summary, summary_path, list(summary[0].keys()))
    write_metadata(out_dir, args, len(rows))
    print(f"Wrote {len(rows)} real-data trials to {trial_path}")
    print(f"Wrote real-data summary to {summary_path}")


if __name__ == "__main__":
    main()
