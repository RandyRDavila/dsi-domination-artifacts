# Dual-Server Independent Domination Artifacts

This repository contains the manuscript source and computational artifacts for
the paper `Dual-Server Independent Domination in Graphs`.

## Contents

- `manuscript/`
  - `ChDaHaHePe2026a_submit.tex`: LaTeX source for the submitted manuscript.
  - `ChDaHaHePe2026a_submit.pdf`: compiled manuscript PDF.
- `computational_data/`
  - scripts, CSV summaries, LP files, CBC logs, solution files, and metadata
    supporting the computational portions of the paper.

## Reproducing The Computations

The computational scripts use Python's standard library and the command-line
CBC solver. Run commands from the repository root.

For the DSI binary integer programming benchmark suite:

```sh
python3 computational_data/benchmark_dsi_mip.py --suite benchmark --time-limit 10
```

For a quick smoke test:

```sh
python3 computational_data/benchmark_dsi_mip.py --suite smoke --time-limit 10
```

For the synthetic ensemble-learning illustration:

```sh
python3 computational_data/ensemble_dsi_experiment.py
```

For the standard-data ensemble-learning illustration:

```sh
python3 computational_data/real_data_dsi_experiment.py
```

See `computational_data/README.md` for more detail about generated files and
metadata.

