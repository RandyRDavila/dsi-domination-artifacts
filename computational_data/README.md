# DSI MIP Benchmarks

This folder contains reproducible computations for the binary integer
programming formulation for dual-server independent domination in
`../manuscript/ChDaHaHePe2026a_submit.tex`.

Run the benchmark suite from the repository root:

```sh
python3 computational_data/benchmark_dsi_mip.py --suite benchmark --time-limit 10
```

For a quick check of the solver and file-writing pipeline, run:

```sh
python3 computational_data/benchmark_dsi_mip.py --suite smoke --time-limit 10
```

The synthetic ensemble-learning appendix experiment can be rerun with:

```sh
python3 computational_data/ensemble_dsi_experiment.py
```

The script uses the command-line CBC solver and only the Python standard
library. It writes:

- `dsi_mip_benchmarks.csv`: instance-level data used for manuscript runtimes.
- `dsi_mip_summary.csv`: aggregate solved counts, median times, maximum
  times, and branch-and-bound statistics by instance family.
- `lp/`: the LP file for each benchmark instance.
- `logs/`: raw CBC output for each benchmark instance.
- `solutions/`: CBC solution files.
- `metadata.txt`: Python, platform, processor, and CBC command information.

Several rows have known theoretical values from the manuscript; the script
checks these values before writing the CSV.

The ensemble experiment writes its outputs to `computational_data/ensemble/`,
including trial-level data, summary data, LP files, CBC logs, solution files,
and metadata.
