#!/usr/bin/env python3
"""Reproducible CBC benchmarks for dual-server independent domination.

The script writes the binary integer program from the manuscript, solves it
with the command-line CBC solver, and records raw LP/log/solution files,
instance-level CSV data, and aggregate summary data.  It intentionally uses
only the Python standard library so the benchmark can be rerun without
Python solver packages.
"""

from __future__ import annotations

import argparse
import csv
import math
import platform
import random
import re
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path


def graph_from_edges(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge endpoint out of range")
        if u == v:
            raise ValueError("loops are not allowed")
        adj[u].add(v)
        adj[v].add(u)
    return tuple(frozenset(nbrs) for nbrs in adj)


def edge_list(adj):
    return [(u, v) for u, nbrs in enumerate(adj) for v in nbrs if u < v]


def is_connected(adj):
    if not adj:
        return True
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for u in adj[v]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == len(adj)


def path_graph(n):
    return graph_from_edges(n, [(i, i + 1) for i in range(n - 1)])


def cycle_graph(n):
    return graph_from_edges(n, [(i, (i + 1) % n) for i in range(n)])


def complete_graph(n):
    return graph_from_edges(n, [(i, j) for i in range(n) for j in range(i + 1, n)])


def complete_bipartite(r, s):
    return graph_from_edges(r + s, [(i, r + j) for i in range(r) for j in range(s)])


def star_graph(n):
    return graph_from_edges(n, [(0, i) for i in range(1, n)])


def cube_graph():
    edges = []
    for u in range(8):
        for bit in range(3):
            v = u ^ (1 << bit)
            if u < v:
                edges.append((u, v))
    return graph_from_edges(8, edges)


def petersen_graph():
    edges = []
    for i in range(5):
        edges.append((i, (i + 1) % 5))
        edges.append((i, i + 5))
        edges.append((i + 5, ((i + 2) % 5) + 5))
    return graph_from_edges(10, edges)


def grid_graph(rows, cols):
    edges = []
    for i in range(rows):
        for j in range(cols):
            v = i * cols + j
            if i + 1 < rows:
                edges.append((v, (i + 1) * cols + j))
            if j + 1 < cols:
                edges.append((v, i * cols + j + 1))
    return graph_from_edges(rows * cols, edges)


def erdos_renyi_connected(n, p, seed):
    rng = random.Random(seed)
    for _ in range(1000):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    edges.append((i, j))
        adj = graph_from_edges(n, edges)
        if is_connected(adj):
            return adj
    raise RuntimeError(f"failed to generate connected G({n},{p}) with seed {seed}")


def random_regular_connected(n, degree, seed):
    if n * degree % 2:
        raise ValueError("n times degree must be even")
    rng = random.Random(seed)
    for _ in range(5000):
        stubs = [v for v in range(n) for _ in range(degree)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i + 1]
            if u == v:
                ok = False
                break
            edge = (u, v) if u < v else (v, u)
            if edge in edges:
                ok = False
                break
            edges.add(edge)
        if ok:
            adj = graph_from_edges(n, edges)
            if is_connected(adj):
                return adj
    raise RuntimeError(f"failed to generate connected {degree}-regular graph")


def path_expected(n):
    return math.ceil((n + 1) / 2)


def cycle_expected(n):
    if n % 4 in (1, 2):
        return math.ceil((n + 2) / 2)
    return math.ceil(n / 2)


def instance(name, family, group, parameters, graph, expected="", seed=""):
    return {
        "name": name,
        "family": family,
        "group": group,
        "parameters": parameters,
        "graph": graph,
        "expected": expected,
        "seed": seed,
    }


def smoke_instances():
    return [
        instance("P20", "path", "paths", "n=20", path_graph(20), path_expected(20)),
        instance("C20", "cycle", "cycles", "n=20", cycle_graph(20), cycle_expected(20)),
        instance("K12", "complete", "complete graphs", "n=12", complete_graph(12), 2),
        instance(
            "K4_8",
            "complete bipartite",
            "complete bipartite",
            "r=4,s=8",
            complete_bipartite(4, 8),
            4,
        ),
        instance("S20", "star", "stars", "n=20", star_graph(20), 19),
        instance("Q3", "cube", "named graphs", "3-cube", cube_graph()),
        instance("Petersen", "Petersen", "named graphs", "standard", petersen_graph()),
        instance(
            "G16_p035_s7",
            "Erdos-Renyi",
            "ER p=0.35",
            "n=16,p=0.35,seed=7",
            erdos_renyi_connected(16, 0.35, 7),
            seed=7,
        ),
        instance(
            "G20_p025_s11",
            "Erdos-Renyi",
            "ER p=0.25",
            "n=20,p=0.25,seed=11",
            erdos_renyi_connected(20, 0.25, 11),
            seed=11,
        ),
    ]


def benchmark_instances(seeds=range(10)):
    items = []

    for n in (20, 40, 60):
        items.append(instance(f"P{n}", "path", "paths", f"n={n}", path_graph(n), path_expected(n)))
        items.append(instance(f"C{n}", "cycle", "cycles", f"n={n}", cycle_graph(n), cycle_expected(n)))
        items.append(instance(f"S{n}", "star", "stars", f"n={n}", star_graph(n), n - 1))

    for n in (12, 20, 30):
        items.append(instance(f"K{n}", "complete", "complete graphs", f"n={n}", complete_graph(n), 2))

    for r, s in ((4, 8), (6, 12), (8, 16)):
        items.append(
            instance(
                f"K{r}_{s}",
                "complete bipartite",
                "complete bipartite",
                f"r={r},s={s}",
                complete_bipartite(r, s),
                r,
            )
        )

    for rows, cols in ((4, 5), (5, 6), (6, 6)):
        items.append(
            instance(
                f"Grid{rows}x{cols}",
                "grid",
                "grids",
                f"{rows}x{cols}",
                grid_graph(rows, cols),
            )
        )

    items.append(instance("Q3", "cube", "named graphs", "3-cube", cube_graph()))
    items.append(instance("Petersen", "Petersen", "named graphs", "standard", petersen_graph()))

    for n in (20, 30, 40):
        for seed in seeds:
            items.append(
                instance(
                    f"ER_n{n}_p020_s{seed}",
                    "Erdos-Renyi",
                    "ER p=0.20",
                    f"n={n},p=0.20,seed={seed}",
                    erdos_renyi_connected(n, 0.20, seed),
                    seed=seed,
                )
            )
            items.append(
                instance(
                    f"ER_n{n}_p035_s{seed}",
                    "Erdos-Renyi",
                    "ER p=0.35",
                    f"n={n},p=0.35,seed={seed}",
                    erdos_renyi_connected(n, 0.35, seed),
                    seed=seed,
                )
            )
            items.append(
                instance(
                    f"Reg3_n{n}_s{seed}",
                    "3-regular",
                    "3-regular",
                    f"n={n},seed={seed}",
                    random_regular_connected(n, 3, seed),
                    seed=seed,
                )
            )

    return items


def lp_sum(terms):
    terms = list(terms)
    # CBC can misread long LP lines if a line break leaves "+" as a separate
    # token.  Attaching the sign to the following variable keeps long dense
    # instances parseable while preserving ordinary LP syntax.
    return " +".join(terms) if terms else "0"


def write_linear_row(f, name, terms, sense=None, rhs=None, width=90):
    terms = list(terms)
    if not terms:
        expression = ["0"]
    else:
        expression = [terms[0]] + [f"+{term}" for term in terms[1:]]

    line = f" {name}:"
    for token in expression:
        piece = f" {token}"
        if len(line) + len(piece) > width and line.strip() != f"{name}:":
            f.write(line + "\n")
            line = f"  {token}"
        else:
            line += piece

    if sense is not None:
        tail = f" {sense} {rhs}"
        if len(line) + len(tail) > width:
            f.write(line + "\n")
            line = f"  {tail.strip()}"
        else:
            line += tail
    f.write(line + "\n")


def write_dsi_lp(adj, path):
    n = len(adj)
    edges = edge_list(adj)
    r = [f"r_{v}" for v in range(n)]
    b = [f"b_{v}" for v in range(n)]

    with path.open("w", encoding="utf-8") as f:
        f.write("Minimize\n")
        write_linear_row(f, "obj", r + b)
        f.write("Subject To\n")
        write_linear_row(f, "red_nonempty", r, ">=", 1)
        write_linear_row(f, "blue_nonempty", b, ">=", 1)

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


def parse_solution(path):
    status = ""
    objective = ""
    values = {}
    if not path.exists():
        return status, objective, values
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "Optimal":
            status = "Optimal"
            match = re.search(r"objective value\s+([-+0-9.eE]+)", line)
            if match:
                objective = float(match.group(1))
            continue
        if line.startswith("Stopped"):
            status = "Stopped"
            match = re.search(r"objective value\s+([-+0-9.eE]+)", line)
            if match:
                objective = float(match.group(1))
            continue
        if line.startswith("Infeasible") or line.startswith("Integer infeasible"):
            status = "Infeasible"
            continue
        if len(parts) >= 3 and parts[0].isdigit():
            values[parts[1]] = float(parts[2])
    return status, objective, values


def parse_cbc_stdout(text):
    result = {
        "cbc_objective": "",
        "cbc_lower_bound": "",
        "cbc_gap": "",
        "cbc_nodes": "",
        "cbc_iterations": "",
        "cbc_wall_time": "",
    }
    patterns = {
        "cbc_objective": r"Objective value:\s+([-+0-9.eE]+)",
        "cbc_lower_bound": r"Lower bound:\s+([-+0-9.eE]+)",
        "cbc_gap": r"Gap:\s+([-+0-9.eE]+)",
        "cbc_nodes": r"Enumerated nodes:\s+([0-9]+)",
        "cbc_iterations": r"Total iterations:\s+([0-9]+)",
        "cbc_wall_time": r"Time \(Wallclock seconds\):\s+([-+0-9.eE]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            result[key] = match.group(1)
    return result


def cbc_version(cbc_cmd):
    try:
        result = subprocess.run(
            [cbc_cmd, "-stop"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except OSError:
        return "unavailable"
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    version_lines = [line for line in lines if line.startswith("Welcome") or line.startswith("Version")]
    return "; ".join(version_lines) if version_lines else (lines[0] if lines else "")


def solve_with_cbc(lp_path, sol_path, log_path, cbc_cmd, time_limit):
    command = [cbc_cmd, str(lp_path)]
    if time_limit:
        command.extend(["seconds", str(time_limit)])
    command.extend(["solve", "solu", str(sol_path)])

    start = time.perf_counter()
    completed = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    elapsed = time.perf_counter() - start
    log_path.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout)
    status, objective, values = parse_solution(sol_path)
    parsed_log = parse_cbc_stdout(completed.stdout)
    return status, objective, values, parsed_log, elapsed


def selected_vertices(values, prefix, n):
    return [str(v) for v in range(n) if values.get(f"{prefix}_{v}", 0.0) > 0.5]


def sanitize(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def run_instances(items, out_dir, cbc_cmd, time_limit):
    lp_dir = out_dir / "lp"
    log_dir = out_dir / "logs"
    sol_dir = out_dir / "solutions"
    for directory, pattern in ((lp_dir, "*.lp"), (log_dir, "*.log"), (sol_dir, "*.sol")):
        directory.mkdir(parents=True, exist_ok=True)
        for old_file in directory.glob(pattern):
            old_file.unlink()

    rows = []
    for index, item in enumerate(items, start=1):
        adj = item["graph"]
        base = sanitize(item["name"])
        lp_path = lp_dir / f"{base}.lp"
        sol_path = sol_dir / f"{base}.sol"
        log_path = log_dir / f"{base}.log"
        write_dsi_lp(adj, lp_path)
        status, objective, values, parsed_log, elapsed = solve_with_cbc(
            lp_path, sol_path, log_path, cbc_cmd, time_limit
        )
        n = len(adj)
        red = selected_vertices(values, "r", n)
        blue = selected_vertices(values, "b", n)
        gamma = int(round(objective)) if objective != "" else ""
        expected = item["expected"]
        check = ""
        if expected != "":
            check = "pass" if gamma == expected and status == "Optimal" else "fail"
            if check == "fail":
                raise AssertionError(f"{item['name']}: expected {expected}, got {gamma}")
        rows.append(
            {
                "index": index,
                "instance": item["name"],
                "family": item["family"],
                "group": item["group"],
                "parameters": item["parameters"],
                "seed": item["seed"],
                "n": n,
                "m": len(edge_list(adj)),
                "gamma_dsi": gamma,
                "expected_gamma_dsi": expected,
                "known_value_check": check,
                "status": status,
                "wall_time_seconds": f"{elapsed:.6f}",
                "cbc_wall_time_seconds": parsed_log["cbc_wall_time"],
                "cbc_gap": parsed_log["cbc_gap"],
                "cbc_lower_bound": parsed_log["cbc_lower_bound"],
                "cbc_nodes": parsed_log["cbc_nodes"],
                "cbc_iterations": parsed_log["cbc_iterations"],
                "red_size": len(red),
                "blue_size": len(blue),
                "red_vertices": " ".join(red),
                "blue_vertices": " ".join(blue),
                "lp_file": str(lp_path.relative_to(out_dir)),
                "log_file": str(log_path.relative_to(out_dir)),
                "solution_file": str(sol_path.relative_to(out_dir)),
            }
        )
    return rows


def to_float(value):
    if value in ("", None):
        return None
    return float(value)


def to_int(value):
    if value in ("", None):
        return None
    return int(float(value))


def aggregate_rows(rows):
    groups = {}
    for row in rows:
        groups.setdefault(row["group"], []).append(row)

    summary = []
    for group in sorted(groups):
        group_rows = groups[group]
        times = [to_float(row["wall_time_seconds"]) for row in group_rows]
        times = [value for value in times if value is not None]
        cbc_times = [to_float(row["cbc_wall_time_seconds"]) for row in group_rows]
        cbc_times = [value for value in cbc_times if value is not None]
        nodes = [to_int(row["cbc_nodes"]) for row in group_rows]
        nodes = [value for value in nodes if value is not None]
        iterations = [to_int(row["cbc_iterations"]) for row in group_rows]
        iterations = [value for value in iterations if value is not None]
        orders = sorted({int(row["n"]) for row in group_rows})
        edges = [int(row["m"]) for row in group_rows]
        statuses = [row["status"] for row in group_rows]
        solved = sum(1 for status in statuses if status == "Optimal")
        summary.append(
            {
                "group": group,
                "family_values": "; ".join(sorted({row["family"] for row in group_rows})),
                "instances": len(group_rows),
                "orders": ",".join(str(n) for n in orders),
                "min_edges": min(edges),
                "max_edges": max(edges),
                "solved_optimal": solved,
                "median_wall_time_seconds": f"{statistics.median(times):.6f}" if times else "",
                "max_wall_time_seconds": f"{max(times):.6f}" if times else "",
                "median_cbc_wall_time_seconds": f"{statistics.median(cbc_times):.6f}"
                if cbc_times
                else "",
                "max_cbc_wall_time_seconds": f"{max(cbc_times):.6f}" if cbc_times else "",
                "median_cbc_nodes": f"{statistics.median(nodes):.1f}" if nodes else "",
                "max_cbc_nodes": max(nodes) if nodes else "",
                "median_cbc_iterations": f"{statistics.median(iterations):.1f}" if iterations else "",
                "max_cbc_iterations": max(iterations) if iterations else "",
            }
        )
    return summary


def write_csv(rows, path, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(out_dir, cbc_cmd, suite, time_limit, row_count):
    text = "\n".join(
        [
            "DSI MIP benchmark metadata",
            "==========================",
            f"Suite: {suite}",
            f"Instances: {row_count}",
            f"Time limit per instance: {time_limit} seconds",
            f"Python: {sys.version.split()[0]}",
            f"Platform: {platform.platform()}",
            f"Processor: {platform.processor()}",
            f"CBC command: {cbc_cmd}",
            f"CBC version: {cbc_version(cbc_cmd)}",
            "",
            "Rerun from the teresa-dom directory with:",
            f"python3 computational_data/benchmark_dsi_mip.py --suite {suite} --time-limit {time_limit}",
            "",
        ]
    )
    (out_dir / "metadata.txt").write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        default="computational_data",
        help="directory for CSV, LP files, logs, and solutions",
    )
    parser.add_argument(
        "--cbc",
        default=shutil.which("cbc") or "cbc",
        help="path to the CBC executable",
    )
    parser.add_argument(
        "--suite",
        choices=("smoke", "benchmark"),
        default="benchmark",
        help="small smoke test or the benchmark suite used in the manuscript",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=10.0,
        help="CBC time limit in seconds for each instance",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    items = smoke_instances() if args.suite == "smoke" else benchmark_instances()
    rows = run_instances(items, out_dir, args.cbc, args.time_limit)
    summary = aggregate_rows(rows)

    instance_fields = [
        "index",
        "instance",
        "family",
        "group",
        "parameters",
        "seed",
        "n",
        "m",
        "gamma_dsi",
        "expected_gamma_dsi",
        "known_value_check",
        "status",
        "wall_time_seconds",
        "cbc_wall_time_seconds",
        "cbc_gap",
        "cbc_lower_bound",
        "cbc_nodes",
        "cbc_iterations",
        "red_size",
        "blue_size",
        "red_vertices",
        "blue_vertices",
        "lp_file",
        "log_file",
        "solution_file",
    ]
    summary_fields = [
        "group",
        "family_values",
        "instances",
        "orders",
        "min_edges",
        "max_edges",
        "solved_optimal",
        "median_wall_time_seconds",
        "max_wall_time_seconds",
        "median_cbc_wall_time_seconds",
        "max_cbc_wall_time_seconds",
        "median_cbc_nodes",
        "max_cbc_nodes",
        "median_cbc_iterations",
        "max_cbc_iterations",
    ]

    write_csv(rows, out_dir / "dsi_mip_benchmarks.csv", instance_fields)
    write_csv(summary, out_dir / "dsi_mip_summary.csv", summary_fields)
    write_metadata(out_dir, args.cbc, args.suite, args.time_limit, len(rows))
    print(f"Wrote {len(rows)} instance rows to {out_dir / 'dsi_mip_benchmarks.csv'}")
    print(f"Wrote {len(summary)} summary rows to {out_dir / 'dsi_mip_summary.csv'}")


if __name__ == "__main__":
    main()
