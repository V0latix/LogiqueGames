# Queens Benchmark Report

- Generated: 2026-01-27 23:16:03
- Dataset: `data/imported/queens/samimsu`
- Algorithms: baseline, heuristic_lcv, heuristic_simple
- Time limit: 0.5s

## Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 473 | 450 | 95.14% | 24.626 | 0.732 | 67757.6 | 5787.9 |
| heuristic_lcv | 473 | 421 | 89.01% | 27.391 | 1.705 | 871.9 | 478.6 |
| heuristic_simple | 473 | 429 | 90.70% | 31.951 | 1.782 | 1508.8 | 843.4 |

## Charts

### Average Time (ms)

```text
baseline           | ########################         |     24.626
heuristic_lcv      | ###########################      |     27.391
heuristic_simple   | ################################ |     31.951
```

### Average Nodes

```text
baseline           | ################################ |  67757.602
heuristic_lcv      | #                                |    871.891
heuristic_simple   | #                                |   1508.793
```

## Slowest Puzzles

### Slowest Puzzles (by time)

```text
baseline:
  samimsu_level263     |    492.977 ms | nodes=1427910
  samimsu_level215     |    490.043 ms | nodes=1414830
  samimsu_level214     |    410.531 ms | nodes=1171635
heuristic_simple:
  samimsu_level193     |    493.767 ms | nodes=29106
  samimsu_level273     |    485.413 ms | nodes=7147
  samimsu_level76      |    435.479 ms | nodes=23880
heuristic_lcv:
  samimsu_level412     |    496.750 ms | nodes=19627
  samimsu_level248     |    484.591 ms | nodes=12178
  samimsu_level276     |    462.741 ms | nodes=15151
```

## Timeouts

### Timeouts by Algorithm

```text
baseline           |  23 / 473 |   4.86%
heuristic_lcv      |  52 / 473 |  10.99%
heuristic_simple   |  44 / 473 |   9.30%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.