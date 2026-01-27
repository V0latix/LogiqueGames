# Queens Benchmark Report (Recursive)

- Generated: 2026-01-28 00:05:59
- Dataset root: `data/generated/queens`
- Algorithms: baseline, csp_ac3, dlx, heuristic_lcv, heuristic_simple
- Time limit: 0.5s

## Global Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 450 | 450 | 100.00% | 0.769 | 0.729 | 11.6 | 2.9 |
| heuristic_lcv | 450 | 450 | 100.00% | 2.361 | 0.947 | 67.5 | 33.0 |
| baseline | 450 | 450 | 100.00% | 2.445 | 0.089 | 6731.3 | 582.7 |
| csp_ac3 | 450 | 450 | 100.00% | 4.265 | 1.765 | 30.7 | 21.9 |
| heuristic_simple | 450 | 449 | 99.78% | 6.037 | 0.426 | 332.7 | 197.9 |

## Size 10

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 70 | 70 | 100.00% | 0.914 | 0.786 | 14.7 | 4.7 |
| baseline | 70 | 70 | 100.00% | 1.537 | 0.225 | 4189.0 | 413.4 |
| heuristic_lcv | 70 | 70 | 100.00% | 1.823 | 1.433 | 35.3 | 14.6 |
| csp_ac3 | 70 | 70 | 100.00% | 3.147 | 2.590 | 18.0 | 8.0 |
| heuristic_simple | 70 | 70 | 100.00% | 5.375 | 1.010 | 360.7 | 207.6 |

### Average Time (ms)

```text
dlx                | #####                            |      0.914
baseline           | #########                        |      1.537
heuristic_lcv      | ##########                       |      1.823
csp_ac3            | ##################               |      3.147
heuristic_simple   | ################################ |      5.375
```

### Average Nodes

```text
dlx                | #                                |     14.700
baseline           | ################################ |   4189.000
heuristic_lcv      | #                                |     35.343
csp_ac3            | #                                |     17.957
heuristic_simple   | ##                               |    360.714
```

### Slowest Puzzles (by time)

```text
baseline:
  size_10/queens_n10_018_seed198 |     51.566 ms | nodes=141795
  size_10/queens_n10_035_seed435 |     10.589 ms | nodes=29065
  size_10/queens_n10_010_seed410 |      5.856 ms | nodes=16275
heuristic_simple:
  size_10/queens_n10_018_seed198 |    184.933 ms | nodes=13931
  size_10/queens_n10_005_seed405 |     21.768 ms | nodes=1407
  size_10/queens_n10_041_seed441 |     20.488 ms | nodes=1043
heuristic_lcv:
  size_10/queens_n10_020_seed420 |      5.627 ms | nodes=185
  size_10/queens_n10_034_seed434 |      5.021 ms | nodes=194
  size_10/queens_n10_044_seed444 |      4.281 ms | nodes=119
dlx:
  size_10/queens_n10_004_seed184 |      2.086 ms | nodes=10
  size_10/queens_n10_040_seed440 |      1.888 ms | nodes=119
  size_10/queens_n10_007_seed187 |      1.791 ms | nodes=10
csp_ac3:
  size_10/queens_n10_034_seed434 |      9.181 ms | nodes=93
  size_10/queens_n10_045_seed445 |      6.797 ms | nodes=61
  size_10/queens_n10_020_seed420 |      6.330 ms | nodes=49
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
```

## Size 11

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 50 | 50 | 100.00% | 1.050 | 0.938 | 16.4 | 5.4 |
| baseline | 50 | 50 | 100.00% | 4.335 | 0.987 | 11951.3 | 1080.5 |
| heuristic_lcv | 50 | 50 | 100.00% | 4.791 | 2.116 | 141.6 | 74.7 |
| csp_ac3 | 50 | 50 | 100.00% | 8.065 | 3.869 | 51.3 | 40.3 |
| heuristic_simple | 50 | 50 | 100.00% | 12.549 | 3.437 | 675.1 | 412.5 |

### Average Time (ms)

```text
dlx                | ##                               |      1.050
baseline           | ###########                      |      4.335
heuristic_lcv      | ############                     |      4.791
csp_ac3            | ####################             |      8.065
heuristic_simple   | ################################ |     12.549
```

### Average Nodes

```text
dlx                | #                                |     16.440
baseline           | ################################ |  11951.280
heuristic_lcv      | #                                |    141.600
csp_ac3            | #                                |     51.340
heuristic_simple   | #                                |    675.060
```

### Slowest Puzzles (by time)

```text
baseline:
  size_11/queens_n11_038_seed488 |     73.988 ms | nodes=204820
  size_11/queens_n11_037_seed487 |     52.348 ms | nodes=143781
  size_11/queens_n11_020_seed470 |     18.600 ms | nodes=50963
heuristic_simple:
  size_11/queens_n11_038_seed488 |    312.019 ms | nodes=16517
  size_11/queens_n11_020_seed470 |     74.753 ms | nodes=4407
  size_11/queens_n11_039_seed489 |     52.709 ms | nodes=2988
heuristic_lcv:
  size_11/queens_n11_041_seed491 |    110.197 ms | nodes=4958
  size_11/queens_n11_044_seed494 |      8.426 ms | nodes=253
  size_11/queens_n11_011_seed461 |      8.413 ms | nodes=328
dlx:
  size_11/queens_n11_005_seed455 |      4.815 ms | nodes=11
  size_11/queens_n11_017_seed467 |      1.690 ms | nodes=79
  size_11/queens_n11_025_seed475 |      1.441 ms | nodes=60
csp_ac3:
  size_11/queens_n11_041_seed491 |    161.772 ms | nodes=1427
  size_11/queens_n11_011_seed461 |     16.079 ms | nodes=146
  size_11/queens_n11_017_seed467 |     13.304 ms | nodes=113
```

### Timeouts by Algorithm

```text
baseline           |   0 /  50 |   0.00%
csp_ac3            |   0 /  50 |   0.00%
dlx                |   0 /  50 |   0.00%
heuristic_lcv      |   0 /  50 |   0.00%
heuristic_simple   |   0 /  50 |   0.00%
```

## Size 12

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 50 | 50 | 100.00% | 1.376 | 1.299 | 16.4 | 4.4 |
| heuristic_lcv | 50 | 50 | 100.00% | 10.264 | 3.080 | 317.5 | 170.8 |
| baseline | 50 | 50 | 100.00% | 14.904 | 1.760 | 41373.8 | 3441.3 |
| csp_ac3 | 50 | 50 | 100.00% | 19.339 | 5.325 | 138.7 | 126.7 |
| heuristic_simple | 50 | 49 | 98.00% | 32.169 | 5.513 | 1665.9 | 1016.3 |

### Average Time (ms)

```text
dlx                | #                                |      1.376
heuristic_lcv      | ##########                       |     10.264
baseline           | ##############                   |     14.904
csp_ac3            | ###################              |     19.339
heuristic_simple   | ################################ |     32.169
```

### Average Nodes

```text
dlx                | #                                |     16.360
heuristic_lcv      | #                                |    317.460
baseline           | ################################ |  41373.840
csp_ac3            | #                                |    138.740
heuristic_simple   | #                                |   1665.918
```

### Slowest Puzzles (by time)

```text
baseline:
  size_12/queens_n12_047_seed547 |    241.797 ms | nodes=672570
  size_12/queens_n12_038_seed538 |     91.738 ms | nodes=255882
  size_12/queens_n12_014_seed514 |     67.967 ms | nodes=187314
heuristic_simple:
  size_12/queens_n12_014_seed514 |    236.687 ms | nodes=14886
  size_12/queens_n12_037_seed537 |    193.497 ms | nodes=9566
  size_12/queens_n12_033_seed533 |    179.218 ms | nodes=8326
heuristic_lcv:
  size_12/queens_n12_030_seed530 |    161.473 ms | nodes=6006
  size_12/queens_n12_014_seed514 |    140.276 ms | nodes=6115
  size_12/queens_n12_003_seed503 |     18.535 ms | nodes=614
dlx:
  size_12/queens_n12_048_seed548 |      4.536 ms | nodes=12
  size_12/queens_n12_034_seed534 |      1.914 ms | nodes=12
  size_12/queens_n12_047_seed547 |      1.797 ms | nodes=63
csp_ac3:
  size_12/queens_n12_014_seed514 |    302.713 ms | nodes=2701
  size_12/queens_n12_030_seed530 |    294.465 ms | nodes=2567
  size_12/queens_n12_003_seed503 |     34.280 ms | nodes=263
```

### Timeouts by Algorithm

```text
baseline           |   0 /  50 |   0.00%
csp_ac3            |   0 /  50 |   0.00%
dlx                |   0 /  50 |   0.00%
heuristic_lcv      |   0 /  50 |   0.00%
heuristic_simple   |   1 /  50 |   2.00%
```

## Size 6

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.032 | 0.025 | 53.1 | 5.3 |
| heuristic_simple | 70 | 70 | 100.00% | 0.125 | 0.111 | 11.2 | 2.9 |
| heuristic_lcv | 70 | 70 | 100.00% | 0.257 | 0.230 | 12.0 | 3.2 |
| dlx | 70 | 70 | 100.00% | 0.346 | 0.273 | 6.9 | 0.9 |
| csp_ac3 | 70 | 70 | 100.00% | 0.448 | 0.412 | 7.8 | 1.8 |

### Average Time (ms)

```text
baseline           | ##                               |      0.032
heuristic_simple   | ########                         |      0.125
heuristic_lcv      | ##################               |      0.257
dlx                | ########################         |      0.346
csp_ac3            | ################################ |      0.448
```

### Average Nodes

```text
baseline           | ################################ |     53.057
heuristic_simple   | ######                           |     11.214
heuristic_lcv      | #######                          |     11.957
dlx                | ####                             |      6.943
csp_ac3            | ####                             |      7.757
```

### Slowest Puzzles (by time)

```text
baseline:
  size_6/queens_n6_022_seed222 |      0.098 ms | nodes=207
  size_6/queens_n6_009_seed109 |      0.093 ms | nodes=189
  size_6/queens_n6_005_seed105 |      0.091 ms | nodes=189
heuristic_simple:
  size_6/queens_n6_009_seed109 |      0.334 ms | nodes=33
  size_6/queens_n6_022_seed222 |      0.323 ms | nodes=31
  size_6/queens_n6_005_seed105 |      0.317 ms | nodes=34
heuristic_lcv:
  size_6/queens_n6_022_seed222 |      0.748 ms | nodes=51
  size_6/queens_n6_007_seed207 |      0.610 ms | nodes=40
  size_6/queens_n6_003_seed103 |      0.426 ms | nodes=28
dlx:
  size_6/queens_n6_012_seed112 |      2.204 ms | nodes=9
  size_6/queens_n6_020_seed220 |      1.320 ms | nodes=6
  size_6/queens_n6_030_seed230 |      0.953 ms | nodes=10
csp_ac3:
  size_6/queens_n6_022_seed222 |      1.160 ms | nodes=26
  size_6/queens_n6_007_seed207 |      0.905 ms | nodes=18
  size_6/queens_n6_018_seed118 |      0.697 ms | nodes=15
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
```

## Size 7

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.057 | 0.038 | 111.2 | 11.9 |
| heuristic_simple | 70 | 70 | 100.00% | 0.244 | 0.179 | 18.9 | 6.8 |
| heuristic_lcv | 70 | 70 | 100.00% | 0.459 | 0.405 | 15.9 | 4.8 |
| dlx | 70 | 70 | 100.00% | 0.507 | 0.393 | 8.5 | 1.5 |
| csp_ac3 | 70 | 70 | 100.00% | 0.823 | 0.737 | 9.9 | 2.9 |

### Average Time (ms)

```text
baseline           | ##                               |      0.057
heuristic_simple   | #########                        |      0.244
heuristic_lcv      | #################                |      0.459
dlx                | ###################              |      0.507
csp_ac3            | ################################ |      0.823
```

### Average Nodes

```text
baseline           | ################################ |    111.200
heuristic_simple   | #####                            |     18.943
heuristic_lcv      | ####                             |     15.900
dlx                | ##                               |      8.500
csp_ac3            | ##                               |      9.914
```

### Slowest Puzzles (by time)

```text
baseline:
  size_7/queens_n7_017_seed137 |      0.367 ms | nodes=847
  size_7/queens_n7_005_seed255 |      0.293 ms | nodes=665
  size_7/queens_n7_014_seed264 |      0.270 ms | nodes=616
heuristic_simple:
  size_7/queens_n7_017_seed137 |      1.241 ms | nodes=124
  size_7/queens_n7_005_seed255 |      0.937 ms | nodes=91
  size_7/queens_n7_014_seed264 |      0.894 ms | nodes=88
heuristic_lcv:
  size_7/queens_n7_026_seed276 |      1.260 ms | nodes=66
  size_7/queens_n7_017_seed137 |      0.819 ms | nodes=48
  size_7/queens_n7_002_seed122 |      0.776 ms | nodes=38
dlx:
  size_7/queens_n7_011_seed131 |      0.916 ms | nodes=7
  size_7/queens_n7_032_seed282 |      0.890 ms | nodes=7
  size_7/queens_n7_022_seed272 |      0.850 ms | nodes=7
csp_ac3:
  size_7/queens_n7_026_seed276 |      1.943 ms | nodes=32
  size_7/queens_n7_014_seed264 |      1.875 ms | nodes=32
  size_7/queens_n7_002_seed122 |      1.466 ms | nodes=22
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
```

## Size 8

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.084 | 0.053 | 182.4 | 18.3 |
| heuristic_simple | 70 | 70 | 100.00% | 0.368 | 0.259 | 24.6 | 9.6 |
| dlx | 70 | 70 | 100.00% | 0.645 | 0.602 | 9.8 | 1.8 |
| heuristic_lcv | 70 | 70 | 100.00% | 0.663 | 0.613 | 15.4 | 4.0 |
| csp_ac3 | 70 | 70 | 100.00% | 1.234 | 1.144 | 10.5 | 2.5 |

### Average Time (ms)

```text
baseline           | ##                               |      0.084
heuristic_simple   | #########                        |      0.368
dlx                | ################                 |      0.645
heuristic_lcv      | #################                |      0.663
csp_ac3            | ################################ |      1.234
```

### Average Nodes

```text
baseline           | ################################ |    182.400
heuristic_simple   | ####                             |     24.614
dlx                | #                                |      9.814
heuristic_lcv      | ##                               |     15.443
csp_ac3            | #                                |     10.543
```

### Slowest Puzzles (by time)

```text
baseline:
  size_8/queens_n8_014_seed314 |      0.424 ms | nodes=1028
  size_8/queens_n8_046_seed346 |      0.278 ms | nodes=652
  size_8/queens_n8_013_seed313 |      0.241 ms | nodes=548
heuristic_simple:
  size_8/queens_n8_014_seed314 |      1.497 ms | nodes=127
  size_8/queens_n8_004_seed304 |      0.980 ms | nodes=59
  size_8/queens_n8_046_seed346 |      0.891 ms | nodes=81
heuristic_lcv:
  size_8/queens_n8_006_seed146 |      1.329 ms | nodes=59
  size_8/queens_n8_045_seed345 |      1.260 ms | nodes=56
  size_8/queens_n8_046_seed346 |      1.052 ms | nodes=43
dlx:
  size_8/queens_n8_039_seed339 |      0.960 ms | nodes=22
  size_8/queens_n8_011_seed311 |      0.947 ms | nodes=9
  size_8/queens_n8_029_seed329 |      0.945 ms | nodes=12
csp_ac3:
  size_8/queens_n8_006_seed146 |      2.643 ms | nodes=37
  size_8/queens_n8_045_seed345 |      2.213 ms | nodes=26
  size_8/queens_n8_046_seed346 |      1.967 ms | nodes=22
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
```

## Size 9

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.267 | 0.120 | 647.9 | 67.0 |
| dlx | 70 | 70 | 100.00% | 0.796 | 0.638 | 11.5 | 2.5 |
| heuristic_simple | 70 | 70 | 100.00% | 1.129 | 0.621 | 70.0 | 36.4 |
| heuristic_lcv | 70 | 70 | 100.00% | 1.220 | 0.987 | 27.4 | 10.2 |
| csp_ac3 | 70 | 70 | 100.00% | 2.195 | 1.823 | 15.4 | 6.4 |

### Average Time (ms)

```text
baseline           | ###                              |      0.267
dlx                | ###########                      |      0.796
heuristic_simple   | ################                 |      1.129
heuristic_lcv      | #################                |      1.220
csp_ac3            | ################################ |      2.195
```

### Average Nodes

```text
baseline           | ################################ |    647.871
dlx                | #                                |     11.486
heuristic_simple   | ###                              |     70.043
heuristic_lcv      | #                                |     27.400
csp_ac3            | #                                |     15.429
```

### Slowest Puzzles (by time)

```text
baseline:
  size_9/queens_n9_019_seed179 |      2.075 ms | nodes=5274
  size_9/queens_n9_007_seed357 |      1.277 ms | nodes=3168
  size_9/queens_n9_020_seed370 |      1.144 ms | nodes=2808
heuristic_simple:
  size_9/queens_n9_019_seed179 |      9.087 ms | nodes=569
  size_9/queens_n9_037_seed387 |      4.869 ms | nodes=311
  size_9/queens_n9_007_seed357 |      4.557 ms | nodes=331
heuristic_lcv:
  size_9/queens_n9_044_seed394 |      8.234 ms | nodes=431
  size_9/queens_n9_038_seed388 |      2.858 ms | nodes=109
  size_9/queens_n9_048_seed398 |      2.491 ms | nodes=106
dlx:
  size_9/queens_n9_013_seed363 |      3.642 ms | nodes=9
  size_9/queens_n9_020_seed370 |      2.423 ms | nodes=16
  size_9/queens_n9_026_seed376 |      1.421 ms | nodes=11
csp_ac3:
  size_9/queens_n9_044_seed394 |     16.099 ms | nodes=222
  size_9/queens_n9_038_seed388 |      3.804 ms | nodes=30
  size_9/queens_n9_048_seed398 |      3.167 ms | nodes=30
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.