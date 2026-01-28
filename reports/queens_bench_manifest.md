# Queens Benchmark Report

- Generated: 2026-01-28 09:26:52
- Dataset: `data/puzzles.json,data/puzzles_generated.json`
- Algorithms: dlx, baseline, heuristic_lcv, csp_ac3, heuristic_simple, min_conflicts
- Time limit: 0.5s

## Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 923 | 923 | 100.00% | 1.337 | 0.832 | 35.8 | 27.0 |
| baseline | 923 | 898 | 97.29% | 12.745 | 0.263 | 34161.8 | 2981.4 |
| heuristic_lcv | 923 | 869 | 94.15% | 13.654 | 1.260 | 420.8 | 227.8 |
| csp_ac3 | 923 | 881 | 95.45% | 14.958 | 1.809 | 100.6 | 92.0 |
| heuristic_simple | 923 | 877 | 95.02% | 18.652 | 0.844 | 875.2 | 493.4 |
| min_conflicts | 923 | 410 | 44.42% | 163.778 | 136.334 | 9609.8 | 1.9 |

## Charts

### Average Time (ms)

```text
dlx                | #                                |      1.337
baseline           | ##                               |     12.745
heuristic_lcv      | ##                               |     13.654
csp_ac3            | ##                               |     14.958
heuristic_simple   | ###                              |     18.652
min_conflicts      | ################################ |    163.778
```

### Average Nodes

```text
dlx                | #                                |     35.815
baseline           | ################################ |  34161.786
heuristic_lcv      | #                                |    420.756
csp_ac3            | #                                |    100.590
heuristic_simple   | #                                |    875.184
min_conflicts      | #########                        |   9609.798
```

## Slowest Puzzles

### Slowest Puzzles (by time)

```text
baseline:
  manifest_144         |    420.385 ms | nodes=1171635
  manifest_143         |    370.529 ms | nodes=1078680
  manifest_123         |    365.268 ms | nodes=1001034
heuristic_simple:
  manifest_161         |    498.240 ms | nodes=7147
  manifest_63          |    448.458 ms | nodes=21263
  manifest_55          |    442.155 ms | nodes=25894
heuristic_lcv:
  manifest_58          |    487.389 ms | nodes=14863
  manifest_78          |    473.318 ms | nodes=15151
  manifest_146         |    427.195 ms | nodes=5365
dlx:
  manifest_166         |     83.857 ms | nodes=3734
  manifest_161         |     65.766 ms | nodes=3803
  manifest_143         |     65.222 ms | nodes=3110
csp_ac3:
  manifest_150         |    481.496 ms | nodes=1690
  manifest_48          |    466.823 ms | nodes=3275
  manifest_13          |    455.027 ms | nodes=4257
min_conflicts:
  manifest_98          |    487.496 ms | nodes=15743
  manifest_286         |    486.694 ms | nodes=35023
  manifest_366         |    486.175 ms | nodes=35002
```

## Timeouts

### Timeouts by Algorithm

```text
baseline           |  25 / 923 |   2.71%
csp_ac3            |  42 / 923 |   4.55%
dlx                |   0 / 923 |   0.00%
heuristic_lcv      |  54 / 923 |   5.85%
heuristic_simple   |  46 / 923 |   4.98%
min_conflicts      | 513 / 923 |  55.58%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.