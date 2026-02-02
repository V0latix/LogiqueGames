# Zip Benchmark Report

Dataset: `data/generated/zip`
Runs: 600
Time limit per run: 1.00s

## Summary

| Algo | Puzzles | Solved | Solve rate | Avg time (ms) | Median time (ms) | Avg nodes | Avg backtracks |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 200 | 200 | 100.0% | 0.20 | 0.03 | 253.5 | 201.2 |
| heuristic | 200 | 200 | 100.0% | 0.87 | 0.40 | 132.6 | 91.9 |
| heuristic_nolcv | 200 | 200 | 100.0% | 0.31 | 0.18 | 51.0 | 24.6 |

## Top slowest solved puzzles

| Algo | Puzzle | N | Time (ms) | Nodes | Backtracks | Source |
|---|---|---:|---:|---:|---:|---|
| baseline | size_5/zip_n5_003_seed3008584 | 5 | 5.41 | 6629 | 6116 | unknown |
| baseline | size_5/zip_n5_012_seed1552582 | 5 | 5.32 | 6400 | 6037 | unknown |
| baseline | size_5/zip_n5_077_seed4289390 | 5 | 3.15 | 3676 | 3225 | unknown |
| heuristic | size_5/zip_n5_034_seed3180248 | 5 | 8.88 | 1358 | 1018 | unknown |
| heuristic | size_5/zip_n5_069_seed5096379 | 5 | 6.43 | 950 | 797 | unknown |
| heuristic | size_5/zip_n5_066_seed5759127 | 5 | 5.54 | 886 | 667 | unknown |
| heuristic_nolcv | size_5/zip_n5_034_seed3180248 | 5 | 2.80 | 427 | 301 | unknown |
| heuristic_nolcv | size_5/zip_n5_069_seed5096379 | 5 | 2.36 | 406 | 301 | unknown |
| heuristic_nolcv | size_5/zip_n5_066_seed5759127 | 5 | 2.23 | 398 | 279 | unknown |

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.