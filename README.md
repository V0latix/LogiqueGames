# linkedin-game-solver

Educational puzzle solver framework in Python. The first implemented game is LinkedIn **Queens**.

## Quickstart

```bash
python -m pytest
ruff check .
```

## CLI

The CLI entrypoint is `lgs`.

Generate and solve a puzzle:

```bash
lgs generate-solve --n 6 --seed 123 --render
```

Generate a dataset (multiple sizes):

```bash
lgs generate-dataset --sizes 6,7,8 --count 20 --seed 100 --algo heuristic_lcv
```

Benchmark a dataset (recursive by size):

```bash
lgs bench \
  --game queens \
  --dataset data/generated/queens \
  --algo baseline,heuristic_simple,heuristic_lcv,dlx \
  --report reports/queens_bench_all.md \
  --recursive \
  --top-k 3 \
  --timelimit 0.5
```

## DLX Solver

We implemented **DLX (Algorithm X with Dancing Links)** for Queens. It models
row/col/region as exact-cover constraints, and adjacency as secondary columns.
See the full explanation in `docs/dlx.md`.

## Min-Conflicts Solver

We also implemented **Min-Conflicts**, a local search solver with random
restarts. It is fast on larger boards but not guaranteed. See
`docs/min_conflicts.md`.

## Notes

- This project is educational only. No live automation on LinkedIn.
