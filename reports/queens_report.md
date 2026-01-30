# Queens Data Science Report

- Source: `data/benchmarks/queens_runs.jsonl`
- Runs: 9708
- Unique puzzles: 1618
- Algorithms: dlx, baseline, heuristic_simple, csp_ac3, heuristic_lcv, min_conflicts

## Summary Table

| algo             |   puzzles |   solved |   solved_rate |   avg_time_ms |   median_time_ms |   avg_nodes |   avg_backtracks |   timeout_rate |
|:-----------------|----------:|---------:|--------------:|--------------:|-----------------:|------------:|-----------------:|---------------:|
| dlx              |      1618 |     1618 |        100    |       1.22142 |         0.719521 |     31.9382 |         23.3894  |           0    |
| baseline         |      1618 |     1600 |         98.89 |      27.5078  |         1.39544  |  67863.3    |       6218.11    |           1.11 |
| heuristic_simple |      1618 |     1573 |         97.22 |      49.643   |         3.40267  |   2360.96   |       1291.91    |           2.78 |
| csp_ac3          |      1618 |     1560 |         96.42 |      52.9032  |         3.22504  |    398.697  |        390.295   |           3.58 |
| heuristic_lcv    |      1618 |     1558 |         96.29 |      53.9175  |         3.62556  |   1689.86   |        924.428   |           3.71 |
| min_conflicts    |      1618 |      195 |         12.05 |     397.914   |       356.767    |  32749.6    |          6.54359 |          85.91 |

## Source Comparison (imported vs generated)

| source    |   runs |   puzzles |   solved |   solved_rate |   avg_time_ms |   median_time_ms |   avg_nodes |   avg_backtracks |   timeout_rate |
|:----------|-------:|----------:|---------:|--------------:|--------------:|-----------------:|------------:|-----------------:|---------------:|
| imported  |   6192 |      1032 |     5075 |         81.96 |       45.2356 |         2.181    |     16916.1 |          1823.73 |          18.04 |
| generated |   3516 |       586 |     3029 |         86.15 |       45.7684 |         0.927833 |     11930.8 |          1589.29 |          12.91 |

## Source x Algo Breakdown

| source    | algo             |   runs |   puzzles |   solved |   solved_rate |   avg_time_ms |   median_time_ms |   avg_nodes |   avg_backtracks |   timeout_rate |
|:----------|:-----------------|-------:|----------:|---------:|--------------:|--------------:|-----------------:|------------:|-----------------:|---------------:|
| generated | dlx              |    586 |       586 |      586 |        100    |      0.610157 |         0.493125 |     11.3259 |          3.76109 |           0    |
| generated | baseline         |    586 |       586 |      586 |        100    |     20.059    |         0.800229 |  49284.5    |       5144.3     |           0    |
| generated | heuristic_simple |    586 |       586 |      586 |        100    |     44.8937   |         2.01421  |   2687.43   |       1486.91    |           0    |
| generated | heuristic_lcv    |    586 |       586 |      582 |         99.32 |     49.8674   |         2.06269  |   1987.26   |       1092.98    |           0.68 |
| generated | csp_ac3          |    586 |       586 |      573 |         97.78 |     52.739    |         2.47483  |    511.721  |        504.211   |           2.22 |
| generated | min_conflicts    |    586 |       586 |      116 |         19.8  |    353.192    |       268.437    |  36435.2    |          7.28448 |          74.57 |
| imported  | dlx              |   1032 |      1032 |     1032 |        100    |      1.56852  |         0.896958 |     43.6424 |         34.5349  |           0    |
| imported  | baseline         |   1032 |      1032 |     1014 |         98.26 |     31.8125   |         1.81979  |  78600.1    |       6838.67    |           1.74 |
| imported  | heuristic_simple |   1032 |      1032 |      987 |         95.64 |     52.4628   |         3.98762  |   2167.13   |       1176.13    |           4.36 |
| imported  | csp_ac3          |   1032 |      1032 |      987 |         95.64 |     52.9985   |         3.6355   |    333.081  |        324.161   |           4.36 |
| imported  | heuristic_lcv    |   1032 |      1032 |      976 |         94.57 |     56.3326   |         4.44263  |   1512.52   |        823.919   |           5.43 |
| imported  | min_conflicts    |   1032 |      1032 |       79 |          7.66 |    463.582    |       429.54     |  27337.8    |          5.4557  |          92.34 |

## Charts

![Average Time](figures/avg_time.png)
![Solve Rate](figures/solve_rate.png)
![Time Distribution](figures/time_box.png)
![Nodes vs Backtracks](figures/nodes_backtracks.png)
![Time by Size](figures/time_by_size.png)
![Solve Rate by Size](figures/solve_rate_by_size.png)