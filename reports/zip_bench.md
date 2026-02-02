# Zip Benchmark Report

Dataset: `data/generated/zip`
Runs: 1000
Time limit per run: 1.00s

## Summary

| Algo | Puzzles | Solved | Solve rate | Avg time (ms) | Median time (ms) | Avg nodes | Avg backtracks |
|---|---:|---:|---:|---:|---:|---:|---:|
| articulation | 200 | 200 | 100.0% | 0.40 | 0.24 | 42.3 | 22.8 |
| baseline | 200 | 200 | 100.0% | 0.20 | 0.04 | 253.5 | 201.2 |
| forced | 200 | 200 | 100.0% | 0.23 | 0.11 | 29.0 | 21.0 |
| heuristic | 200 | 200 | 100.0% | 0.89 | 0.41 | 132.6 | 91.9 |
| heuristic_nolcv | 200 | 200 | 100.0% | 0.31 | 0.18 | 51.0 | 24.6 |

## Top slowest solved puzzles

| Algo | Puzzle | N | Time (ms) | Nodes | Backtracks | Source |
|---|---|---:|---:|---:|---:|---|
| articulation | size_5/zip_n5_034_seed3180248 | 5 | 3.25 | 322 | 298 | unknown |
| articulation | size_5/zip_n5_069_seed5096379 | 5 | 3.03 | 325 | 301 | unknown |
| articulation | size_5/zip_n5_066_seed5759127 | 5 | 2.88 | 303 | 279 | unknown |
| baseline | size_5/zip_n5_003_seed3008584 | 5 | 5.63 | 6629 | 6116 | unknown |
| baseline | size_5/zip_n5_012_seed1552582 | 5 | 5.35 | 6400 | 6037 | unknown |
| baseline | size_5/zip_n5_077_seed4289390 | 5 | 3.13 | 3676 | 3225 | unknown |
| forced | size_5/zip_n5_034_seed3180248 | 5 | 2.38 | 301 | 285 | unknown |
| forced | size_5/zip_n5_066_seed5759127 | 5 | 2.15 | 278 | 262 | unknown |
| forced | size_5/zip_n5_069_seed5096379 | 5 | 1.97 | 261 | 246 | unknown |
| heuristic | size_5/zip_n5_034_seed3180248 | 5 | 8.82 | 1358 | 1018 | unknown |
| heuristic | size_5/zip_n5_069_seed5096379 | 5 | 6.60 | 950 | 797 | unknown |
| heuristic | size_5/zip_n5_066_seed5759127 | 5 | 5.84 | 886 | 667 | unknown |
| heuristic_nolcv | size_5/zip_n5_034_seed3180248 | 5 | 2.60 | 427 | 301 | unknown |
| heuristic_nolcv | size_5/zip_n5_069_seed5096379 | 5 | 2.47 | 406 | 301 | unknown |
| heuristic_nolcv | size_5/zip_n5_066_seed5759127 | 5 | 2.28 | 398 | 279 | unknown |

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.