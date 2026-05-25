#!/usr/bin/env python3
"""Synthetic ensemble experiment for DSI-selected representative learners.

This script is a proof-of-concept companion to the ensemble-learning
discussion in the manuscript.  It simulates base predictors with correlated
errors, constructs a learner-similarity graph from validation error
correlations, solves the DSI binary integer program, and compares the
majority vote of the DSI-selected ensemble with random same-size ensembles.

The experiment is intentionally synthetic and fully reproducible.  It uses
only the Python standard library and the command-line CBC solver.
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
from pathlib import Path

from benchmark_dsi_mip import (
    cbc_version,
    graph_from_edges,
    solve_with_cbc,
    write_dsi_lp,
    selected_vertices,
)


def clamp(value, low, high):
    return max(low, min(high, value))


def model_parameters(seed, groups, learners_per_group, shared_error, individual_error):
    rng = random.Random(seed)
    group_errors = [
        clamp(rng.gauss(shared_error, 0.025), 0.05, 0.35) for _ in range(groups)
    ]
    learner_errors = [
        clamp(rng.gauss(individual_error, 0.020), 0.03, 0.25)
        for _ in range(groups * learners_per_group)
    ]
    return group_errors, learner_errors


def simulate_predictions(seed, group_errors, learner_errors, sample_count, learners_per_group):
    rng = random.Random(seed)
    groups = len(group_errors)
    labels = [1 if rng.random() < 0.5 else -1 for _ in range(sample_count)]
    predictions = []
    errors = []

    for group in range(groups):
        shared_flips = [rng.random() < group_errors[group] for _ in range(sample_count)]
        for offset in range(learners_per_group):
            learner = group * learners_per_group + offset
            learner_errors_row = []
            learner_predictions = []
            for index, label in enumerate(labels):
                flip = shared_flips[index] ^ (rng.random() < learner_errors[learner])
                learner_errors_row.append(1 if flip else 0)
                learner_predictions.append(-label if flip else label)
            errors.append(learner_errors_row)
            predictions.append(learner_predictions)

    return labels, predictions, errors


def phi_correlation(a, b):
    n = len(a)
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    var_a = mean_a * (1 - mean_a)
    var_b = mean_b * (1 - mean_b)
    if var_a <= 0 or var_b <= 0:
        return 0.0
    covariance = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b)) / n
    return covariance / math.sqrt(var_a * var_b)


def build_error_correlation_graph(errors, threshold):
    edges = []
    correlations = []
    for i in range(len(errors)):
        for j in range(i + 1, len(errors)):
            corr = phi_correlation(errors[i], errors[j])
            correlations.append(corr)
            if corr >= threshold:
                edges.append((i, j))
    return graph_from_edges(len(errors), edges), correlations


def majority_vote_accuracy(labels, predictions, selected):
    correct = 0
    for index, label in enumerate(labels):
        vote = sum(predictions[learner][index] for learner in selected)
        if vote > 0:
            guess = 1
        elif vote < 0:
            guess = -1
        else:
            guess = predictions[selected[0]][index]
        correct += guess == label
    return correct / len(labels)


def mean_individual_accuracy(labels, predictions, selected):
    values = []
    for learner in selected:
        correct = sum(predictions[learner][i] == labels[i] for i in range(len(labels)))
        values.append(correct / len(labels))
    return statistics.mean(values)


def average_error_correlation(errors, selected):
    pairs = list(itertools.combinations(selected, 2))
    if not pairs:
        return 0.0
    return statistics.mean(phi_correlation(errors[i], errors[j]) for i, j in pairs)


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


def percentile(value, sample):
    below = sum(x < value for x in sample)
    equal = sum(x == value for x in sample)
    return (below + 0.5 * equal) / len(sample)


def clean_output_dirs(out_dir):
    for subdir, pattern in (("lp", "*.lp"), ("logs", "*.log"), ("solutions", "*.sol")):
        directory = out_dir / subdir
        directory.mkdir(parents=True, exist_ok=True)
        for old_file in directory.glob(pattern):
            old_file.unlink()


def run_experiment(args):
    out_dir = Path(args.out_dir) / "ensemble"
    out_dir.mkdir(parents=True, exist_ok=True)
    clean_output_dirs(out_dir)

    rows = []
    for trial in range(args.trials):
        group_errors, learner_errors = model_parameters(
            trial,
            args.groups,
            args.learners_per_group,
            args.shared_error,
            args.individual_error,
        )
        validation_labels, validation_predictions, validation_errors = simulate_predictions(
            10000 + trial,
            group_errors,
            learner_errors,
            args.validation_samples,
            args.learners_per_group,
        )
        test_labels, test_predictions, test_errors = simulate_predictions(
            20000 + trial,
            group_errors,
            learner_errors,
            args.test_samples,
            args.learners_per_group,
        )

        adj, validation_correlations = build_error_correlation_graph(
            validation_errors, args.correlation_threshold
        )
        dsi = solve_dsi_partition(adj, out_dir, f"trial_{trial:03d}", args.cbc, args.time_limit)
        selected = dsi["red"] + dsi["blue"]

        rng = random.Random(30000 + trial)
        random_accuracies = []
        random_correlations = []
        random_individual_accuracies = []
        learner_count = args.groups * args.learners_per_group
        for _ in range(args.random_samples):
            sample = rng.sample(range(learner_count), len(selected))
            random_accuracies.append(majority_vote_accuracy(test_labels, test_predictions, sample))
            random_correlations.append(average_error_correlation(test_errors, sample))
            random_individual_accuracies.append(
                mean_individual_accuracy(test_labels, test_predictions, sample)
            )

        dsi_accuracy = majority_vote_accuracy(test_labels, test_predictions, selected)
        dsi_corr = average_error_correlation(test_errors, selected)
        dsi_individual_accuracy = mean_individual_accuracy(test_labels, test_predictions, selected)

        rows.append(
            {
                "trial": trial,
                "learners": learner_count,
                "groups": args.groups,
                "learners_per_group": args.learners_per_group,
                "validation_samples": args.validation_samples,
                "test_samples": args.test_samples,
                "correlation_threshold": args.correlation_threshold,
                "graph_edges": sum(len(nbrs) for nbrs in adj) // 2,
                "mean_validation_error_correlation": f"{statistics.mean(validation_correlations):.6f}",
                "gamma_dsi": dsi["objective"],
                "red_size": len(dsi["red"]),
                "blue_size": len(dsi["blue"]),
                "red_vertices": " ".join(str(v) for v in dsi["red"]),
                "blue_vertices": " ".join(str(v) for v in dsi["blue"]),
                "dsi_test_accuracy": f"{dsi_accuracy:.6f}",
                "random_mean_test_accuracy": f"{statistics.mean(random_accuracies):.6f}",
                "random_sd_test_accuracy": f"{statistics.stdev(random_accuracies):.6f}",
                "dsi_minus_random_accuracy": f"{dsi_accuracy - statistics.mean(random_accuracies):.6f}",
                "dsi_accuracy_percentile": f"{percentile(dsi_accuracy, random_accuracies):.6f}",
                "dsi_mean_individual_accuracy": f"{dsi_individual_accuracy:.6f}",
                "random_mean_individual_accuracy": f"{statistics.mean(random_individual_accuracies):.6f}",
                "dsi_avg_error_correlation": f"{dsi_corr:.6f}",
                "random_mean_error_correlation": f"{statistics.mean(random_correlations):.6f}",
                "dsi_minus_random_correlation": f"{dsi_corr - statistics.mean(random_correlations):.6f}",
                "dsi_status": dsi["status"],
                "cbc_wall_time_seconds": dsi["cbc_wall_time"],
                "driver_wall_time_seconds": f"{dsi['elapsed']:.6f}",
                "cbc_nodes": dsi["cbc_nodes"],
                "lp_file": dsi["lp_file"],
                "log_file": dsi["log_file"],
                "solution_file": dsi["solution_file"],
            }
        )

    return out_dir, rows


def write_csv(rows, path, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    def floats(name):
        return [float(row[name]) for row in rows]

    dsi_minus_random = floats("dsi_minus_random_accuracy")
    corr_diff = floats("dsi_minus_random_correlation")
    summary = {
        "trials": len(rows),
        "learners": rows[0]["learners"] if rows else "",
        "groups": rows[0]["groups"] if rows else "",
        "learners_per_group": rows[0]["learners_per_group"] if rows else "",
        "validation_samples": rows[0]["validation_samples"] if rows else "",
        "test_samples": rows[0]["test_samples"] if rows else "",
        "random_samples_per_trial": "",
        "correlation_threshold": rows[0]["correlation_threshold"] if rows else "",
        "optimal_dsi_trials": sum(row["dsi_status"] == "Optimal" for row in rows),
        "mean_gamma_dsi": f"{statistics.mean(floats('gamma_dsi')):.3f}",
        "min_gamma_dsi": f"{min(floats('gamma_dsi')):.0f}",
        "max_gamma_dsi": f"{max(floats('gamma_dsi')):.0f}",
        "mean_graph_edges": f"{statistics.mean(floats('graph_edges')):.3f}",
        "mean_dsi_accuracy": f"{statistics.mean(floats('dsi_test_accuracy')):.6f}",
        "mean_random_accuracy": f"{statistics.mean(floats('random_mean_test_accuracy')):.6f}",
        "mean_accuracy_difference": f"{statistics.mean(dsi_minus_random):.6f}",
        "median_accuracy_difference": f"{statistics.median(dsi_minus_random):.6f}",
        "dsi_accuracy_wins": sum(value > 0 for value in dsi_minus_random),
        "mean_dsi_accuracy_percentile": f"{statistics.mean(floats('dsi_accuracy_percentile')):.6f}",
        "mean_dsi_error_correlation": f"{statistics.mean(floats('dsi_avg_error_correlation')):.6f}",
        "mean_random_error_correlation": f"{statistics.mean(floats('random_mean_error_correlation')):.6f}",
        "mean_correlation_difference": f"{statistics.mean(corr_diff):.6f}",
        "median_correlation_difference": f"{statistics.median(corr_diff):.6f}",
        "mean_driver_wall_time_seconds": f"{statistics.mean(floats('driver_wall_time_seconds')):.6f}",
        "max_driver_wall_time_seconds": f"{max(floats('driver_wall_time_seconds')):.6f}",
    }
    return summary


def write_metadata(out_dir, args, row_count):
    metadata = "\n".join(
        [
            "Synthetic DSI ensemble experiment metadata",
            "==========================================",
            f"Trials: {row_count}",
            f"Learners: {args.groups * args.learners_per_group}",
            f"Groups: {args.groups}",
            f"Learners per group: {args.learners_per_group}",
            f"Validation samples per trial: {args.validation_samples}",
            f"Test samples per trial: {args.test_samples}",
            f"Random same-size ensembles per trial: {args.random_samples}",
            f"Correlation threshold: {args.correlation_threshold}",
            f"CBC time limit per DSI solve: {args.time_limit}",
            f"CBC command: {args.cbc}",
            f"CBC version: {cbc_version(args.cbc)}",
            f"Python: {sys.version.split()[0]}",
            "",
            "Rerun from the teresa-dom directory with:",
            "python3 computational_data/ensemble_dsi_experiment.py",
            "",
        ]
    )
    (out_dir / "metadata.txt").write_text(metadata, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="computational_data")
    parser.add_argument("--cbc", default=shutil.which("cbc") or "cbc")
    parser.add_argument("--time-limit", type=float, default=10.0)
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--groups", type=int, default=6)
    parser.add_argument("--learners-per-group", type=int, default=8)
    parser.add_argument("--validation-samples", type=int, default=1000)
    parser.add_argument("--test-samples", type=int, default=3000)
    parser.add_argument("--random-samples", type=int, default=200)
    parser.add_argument("--shared-error", type=float, default=0.16)
    parser.add_argument("--individual-error", type=float, default=0.09)
    parser.add_argument("--correlation-threshold", type=float, default=0.15)
    args = parser.parse_args()

    out_dir, rows = run_experiment(args)
    summary = summarize(rows)
    summary["random_samples_per_trial"] = args.random_samples

    fieldnames = list(rows[0].keys())
    write_csv(rows, out_dir / "ensemble_dsi_trials.csv", fieldnames)
    write_csv([summary], out_dir / "ensemble_dsi_summary.csv", list(summary.keys()))
    write_metadata(out_dir, args, len(rows))
    print(f"Wrote {len(rows)} ensemble trials to {out_dir / 'ensemble_dsi_trials.csv'}")
    print(f"Wrote ensemble summary to {out_dir / 'ensemble_dsi_summary.csv'}")


if __name__ == "__main__":
    main()
