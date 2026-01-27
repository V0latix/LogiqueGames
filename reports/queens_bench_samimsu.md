# Queens Benchmark Report (Recursive)

- Generated: 2026-01-28 00:13:04
- Dataset root: `data/imported/queens/samimsu_by_size`
- Algorithms: baseline, csp_ac3, dlx, heuristic_lcv, heuristic_simple
- Time limit: 0.5s

## Global Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 473 | 473 | 100.00% | 1.743 | 0.804 | 58.8 | 49.9 |
| baseline | 473 | 448 | 94.71% | 23.033 | 0.772 | 61714.7 | 5390.8 |
| csp_ac3 | 473 | 431 | 91.12% | 25.990 | 1.967 | 173.6 | 165.1 |
| heuristic_lcv | 473 | 420 | 88.79% | 26.780 | 1.738 | 845.0 | 461.0 |
| heuristic_simple | 473 | 427 | 90.27% | 30.457 | 1.853 | 1431.0 | 795.9 |

## Size 10

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 38 | 38 | 100.00% | 1.214 | 0.919 | 25.7 | 15.7 |
| baseline | 38 | 38 | 100.00% | 42.996 | 17.802 | 113921.1 | 11386.6 |
| csp_ac3 | 38 | 38 | 100.00% | 49.871 | 5.161 | 444.7 | 434.7 |
| heuristic_simple | 38 | 36 | 94.74% | 53.227 | 26.857 | 2933.9 | 1528.5 |
| heuristic_lcv | 38 | 37 | 97.37% | 74.502 | 11.902 | 2832.7 | 1432.6 |

### Average Time (ms)

```text
dlx                | #                                |      1.214
baseline           | ##################               |     42.996
csp_ac3            | #####################            |     49.871
heuristic_simple   | ######################           |     53.227
heuristic_lcv      | ################################ |     74.502
```

### Average Nodes

```text
dlx                | #                                |     25.684
baseline           | ################################ | 113921.053
csp_ac3            | #                                |    444.658
heuristic_simple   | #                                |   2933.917
heuristic_lcv      | #                                |   2832.676
```

### Slowest Puzzles (by time)

```text
baseline:
  size_10/samimsu_level290 |    250.923 ms | nodes=658955
  size_10/samimsu_level164 |    225.611 ms | nodes=613435
  size_10/samimsu_level232 |    187.646 ms | nodes=494225
heuristic_simple:
  size_10/samimsu_level190 |    352.542 ms | nodes=21293
  size_10/samimsu_level224 |    213.242 ms | nodes=14777
  size_10/samimsu_level19 |    188.008 ms | nodes=11115
heuristic_lcv:
  size_10/samimsu_level412 |    498.907 ms | nodes=19627
  size_10/samimsu_level224 |    413.361 ms | nodes=18060
  size_10/samimsu_level190 |    348.343 ms | nodes=13917
dlx:
  size_10/samimsu_level190 |      2.872 ms | nodes=194
  size_10/samimsu_level201 |      2.618 ms | nodes=38
  size_10/samimsu_level290 |      2.403 ms | nodes=105
csp_ac3:
  size_10/samimsu_level190 |    452.799 ms | nodes=4257
  size_10/samimsu_level191 |    341.695 ms | nodes=2991
  size_10/samimsu_level164 |    336.284 ms | nodes=3509
```

### Timeouts by Algorithm

```text
baseline           |   0 /  38 |   0.00%
csp_ac3            |   0 /  38 |   0.00%
dlx                |   0 /  38 |   0.00%
heuristic_lcv      |   1 /  38 |   2.63%
heuristic_simple   |   2 /  38 |   5.26%
```

## Size 11

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 81 | 81 | 100.00% | 1.643 | 1.156 | 51.9 | 40.9 |
| csp_ac3 | 81 | 70 | 86.42% | 62.415 | 16.343 | 412.0 | 401.0 |
| baseline | 81 | 72 | 88.89% | 71.684 | 29.411 | 189832.7 | 17251.5 |
| heuristic_lcv | 81 | 67 | 82.72% | 83.463 | 34.014 | 2453.3 | 1385.4 |
| heuristic_simple | 81 | 69 | 85.19% | 117.226 | 70.931 | 5407.2 | 3056.7 |

### Average Time (ms)

```text
dlx                | #                                |      1.643
csp_ac3            | #################                |     62.415
baseline           | ###################              |     71.684
heuristic_lcv      | ######################           |     83.463
heuristic_simple   | ################################ |    117.226
```

### Average Nodes

```text
dlx                | #                                |     51.889
csp_ac3            | #                                |    412.000
baseline           | ################################ | 189832.653
heuristic_lcv      | #                                |   2453.299
heuristic_simple   | #                                |   5407.246
```

### Slowest Puzzles (by time)

```text
baseline:
  size_11/samimsu_level384 |    313.762 ms | nodes=829807
  size_11/samimsu_level40 |    286.389 ms | nodes=749958
  size_11/samimsu_level294 |    285.184 ms | nodes=756525
heuristic_simple:
  size_11/samimsu_level20 |    448.156 ms | nodes=21263
  size_11/samimsu_level76 |    442.840 ms | nodes=23880
  size_11/samimsu_level181 |    436.760 ms | nodes=25894
heuristic_lcv:
  size_11/samimsu_level187 |    484.675 ms | nodes=14863
  size_11/samimsu_level276 |    473.251 ms | nodes=15151
  size_11/samimsu_level317 |    413.610 ms | nodes=10493
dlx:
  size_11/samimsu_level234 |     10.061 ms | nodes=690
  size_11/samimsu_level276 |      4.890 ms | nodes=245
  size_11/samimsu_level307 |      4.510 ms | nodes=194
csp_ac3:
  size_11/samimsu_level142 |    462.669 ms | nodes=3275
  size_11/samimsu_level401 |    322.169 ms | nodes=2304
  size_11/samimsu_level389 |    254.820 ms | nodes=1680
```

### Timeouts by Algorithm

```text
baseline           |   9 /  81 |  11.11%
csp_ac3            |  11 /  81 |  13.58%
dlx                |   0 /  81 |   0.00%
heuristic_lcv      |  14 /  81 |  17.28%
heuristic_simple   |  12 /  81 |  14.81%
```

## Size 12

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heuristic_lcv | 5 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| csp_ac3 | 5 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 5 | 5 | 100.00% | 1.796 | 1.696 | 40.8 | 28.8 |
| baseline | 5 | 3 | 60.00% | 205.152 | 137.584 | 558354.0 | 46523.0 |
| heuristic_simple | 5 | 1 | 20.00% | 373.842 | 373.842 | 17702.0 | 9417.0 |

### Average Time (ms)

```text
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
dlx                | #                                |      1.796
baseline           | #################                |    205.152
heuristic_simple   | ################################ |    373.842
```

### Average Nodes

```text
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
dlx                | #                                |     40.800
baseline           | ################################ | 558354.000
heuristic_simple   | #                                |  17702.000
```

### Slowest Puzzles (by time)

```text
dlx:
  size_12/samimsu_level303 |      2.343 ms | nodes=64
  size_12/samimsu_level204 |      2.125 ms | nodes=64
  size_12/samimsu_level223 |      1.696 ms | nodes=32
baseline:
  size_12/samimsu_level223 |    367.134 ms | nodes=1001034
  size_12/samimsu_level204 |    137.584 ms | nodes=381834
  size_12/samimsu_level202 |    110.739 ms | nodes=292194
heuristic_simple:
  size_12/samimsu_level202 |    373.842 ms | nodes=17702
```

### Timeouts by Algorithm

```text
baseline           |   2 /   5 |  40.00%
csp_ac3            |   5 /   5 | 100.00%
dlx                |   0 /   5 |   0.00%
heuristic_lcv      |   5 /   5 | 100.00%
heuristic_simple   |   4 /   5 |  80.00%
```

## Size 13

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 14 | 14 | 100.00% | 2.886 | 2.148 | 84.0 | 71.0 |
| baseline | 14 | 12 | 85.71% | 46.762 | 5.863 | 128328.4 | 9864.4 |
| heuristic_simple | 14 | 8 | 57.14% | 73.193 | 22.706 | 1929.4 | 1112.2 |
| csp_ac3 | 14 | 7 | 50.00% | 83.370 | 53.035 | 332.1 | 319.1 |
| heuristic_lcv | 14 | 6 | 42.86% | 108.118 | 62.834 | 2342.2 | 1346.3 |

### Average Time (ms)

```text
dlx                | #                                |      2.886
baseline           | #############                    |     46.762
heuristic_simple   | #####################            |     73.193
csp_ac3            | ########################         |     83.370
heuristic_lcv      | ################################ |    108.118
```

### Average Nodes

```text
dlx                | #                                |     84.000
baseline           | ################################ | 128328.417
heuristic_simple   | #                                |   1929.375
csp_ac3            | #                                |    332.143
heuristic_lcv      | #                                |   2342.167
```

### Slowest Puzzles (by time)

```text
baseline:
  size_13/samimsu_level278 |    180.048 ms | nodes=491244
  size_13/samimsu_level244 |    152.741 ms | nodes=416741
  size_13/samimsu_level237 |    145.796 ms | nodes=406874
heuristic_simple:
  size_13/samimsu_level221 |    382.380 ms | nodes=10056
  size_13/samimsu_level219 |     83.255 ms | nodes=2082
  size_13/samimsu_level305 |     55.280 ms | nodes=1414
heuristic_lcv:
  size_13/samimsu_level279 |    348.443 ms | nodes=8227
  size_13/samimsu_level305 |    156.574 ms | nodes=2688
  size_13/samimsu_level195 |     69.949 ms | nodes=1759
dlx:
  size_13/samimsu_level237 |      8.949 ms | nodes=373
  size_13/samimsu_level195 |      5.418 ms | nodes=284
  size_13/samimsu_level226 |      3.773 ms | nodes=104
csp_ac3:
  size_13/samimsu_level279 |    231.142 ms | nodes=1029
  size_13/samimsu_level238 |    177.573 ms | nodes=534
  size_13/samimsu_level278 |     72.739 ms | nodes=341
```

### Timeouts by Algorithm

```text
baseline           |   2 /  14 |  14.29%
csp_ac3            |   7 /  14 |  50.00%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |   8 /  14 |  57.14%
heuristic_simple   |   6 /  14 |  42.86%
```

## Size 14

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 4 | 4 | 100.00% | 3.635 | 2.627 | 111.2 | 97.2 |
| heuristic_lcv | 4 | 1 | 25.00% | 6.913 | 6.913 | 81.0 | 38.0 |
| baseline | 4 | 1 | 25.00% | 13.116 | 13.116 | 35889.0 | 2556.0 |
| csp_ac3 | 4 | 1 | 25.00% | 24.371 | 24.371 | 68.0 | 54.0 |
| heuristic_simple | 4 | 1 | 25.00% | 78.106 | 78.106 | 1695.0 | 1059.0 |

### Average Time (ms)

```text
dlx                | #                                |      3.635
heuristic_lcv      | ##                               |      6.913
baseline           | #####                            |     13.116
csp_ac3            | #########                        |     24.371
heuristic_simple   | ################################ |     78.106
```

### Average Nodes

```text
dlx                | #                                |    111.250
heuristic_lcv      | #                                |     81.000
baseline           | ################################ |  35889.000
csp_ac3            | #                                |     68.000
heuristic_simple   | #                                |   1695.000
```

### Slowest Puzzles (by time)

```text
dlx:
  size_14/samimsu_level212 |      7.380 ms | nodes=335
  size_14/samimsu_level296 |      3.195 ms | nodes=75
  size_14/samimsu_level228 |      2.060 ms | nodes=21
baseline:
  size_14/samimsu_level296 |     13.116 ms | nodes=35889
heuristic_simple:
  size_14/samimsu_level296 |     78.106 ms | nodes=1695
heuristic_lcv:
  size_14/samimsu_level296 |      6.913 ms | nodes=81
csp_ac3:
  size_14/samimsu_level296 |     24.371 ms | nodes=68
```

### Timeouts by Algorithm

```text
baseline           |   3 /   4 |  75.00%
csp_ac3            |   3 /   4 |  75.00%
dlx                |   0 /   4 |   0.00%
heuristic_lcv      |   3 /   4 |  75.00%
heuristic_simple   |   3 /   4 |  75.00%
```

## Size 15

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 14 | 14 | 100.00% | 8.842 | 3.350 | 365.0 | 350.0 |
| heuristic_simple | 14 | 4 | 28.57% | 46.583 | 35.310 | 777.5 | 436.2 |
| baseline | 14 | 11 | 78.57% | 145.763 | 105.382 | 410179.1 | 27337.3 |
| heuristic_lcv | 14 | 3 | 21.43% | 232.443 | 211.655 | 3349.3 | 1935.7 |
| csp_ac3 | 14 | 7 | 50.00% | 254.615 | 214.426 | 734.7 | 719.7 |

### Average Time (ms)

```text
dlx                | #                                |      8.842
heuristic_simple   | #####                            |     46.583
baseline           | ##################               |    145.763
heuristic_lcv      | #############################    |    232.443
csp_ac3            | ################################ |    254.615
```

### Average Nodes

```text
dlx                | #                                |    365.000
heuristic_simple   | #                                |    777.500
baseline           | ################################ | 410179.091
heuristic_lcv      | #                                |   3349.333
csp_ac3            | #                                |    734.714
```

### Slowest Puzzles (by time)

```text
baseline:
  size_15/samimsu_level214 |    426.371 ms | nodes=1171635
  size_15/samimsu_level205 |    378.863 ms | nodes=1078680
  size_15/samimsu_level270 |    258.081 ms | nodes=742395
dlx:
  size_15/samimsu_level205 |     65.462 ms | nodes=3110
  size_15/samimsu_level263 |     13.750 ms | nodes=668
  size_15/samimsu_level306 |      9.141 ms | nodes=504
heuristic_simple:
  size_15/samimsu_level230 |    109.241 ms | nodes=1597
  size_15/samimsu_level271 |     43.509 ms | nodes=690
  size_15/samimsu_level297 |     27.111 ms | nodes=676
heuristic_lcv:
  size_15/samimsu_level230 |    429.289 ms | nodes=5365
  size_15/samimsu_level371 |    211.655 ms | nodes=4062
  size_15/samimsu_level271 |     56.384 ms | nodes=621
csp_ac3:
  size_15/samimsu_level263 |    487.131 ms | nodes=1690
  size_15/samimsu_level245 |    443.916 ms | nodes=1384
  size_15/samimsu_level297 |    342.114 ms | nodes=682
```

### Timeouts by Algorithm

```text
baseline           |   3 /  14 |  21.43%
csp_ac3            |   7 /  14 |  50.00%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |  11 /  14 |  78.57%
heuristic_simple   |  10 /  14 |  71.43%
```

## Size 16

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 7 | 7 | 100.00% | 17.516 | 10.269 | 825.4 | 809.4 |
| baseline | 7 | 5 | 71.43% | 17.932 | 13.069 | 52331.2 | 3262.2 |
| heuristic_lcv | 7 | 1 | 14.29% | 150.780 | 150.780 | 1805.0 | 1144.0 |
| heuristic_simple | 7 | 3 | 42.86% | 162.076 | 169.797 | 2773.3 | 1505.7 |
| csp_ac3 | 7 | 3 | 42.86% | 258.157 | 230.576 | 705.7 | 689.7 |

### Average Time (ms)

```text
dlx                | ##                               |     17.516
baseline           | ##                               |     17.932
heuristic_lcv      | ##################               |    150.780
heuristic_simple   | ####################             |    162.076
csp_ac3            | ################################ |    258.157
```

### Average Nodes

```text
dlx                | #                                |    825.429
baseline           | ################################ |  52331.200
heuristic_lcv      | #                                |   1805.000
heuristic_simple   | #                                |   2773.333
csp_ac3            | #                                |    705.667
```

### Slowest Puzzles (by time)

```text
dlx:
  size_16/samimsu_level273 |     66.190 ms | nodes=3803
  size_16/samimsu_level258 |     21.880 ms | nodes=906
  size_16/samimsu_level253 |     10.396 ms | nodes=357
baseline:
  size_16/samimsu_level273 |     46.164 ms | nodes=134056
  size_16/samimsu_level258 |     22.177 ms | nodes=65208
  size_16/samimsu_level310 |     13.069 ms | nodes=38584
heuristic_simple:
  size_16/samimsu_level258 |    175.727 ms | nodes=2608
  size_16/samimsu_level253 |    169.797 ms | nodes=3344
  size_16/samimsu_level310 |    140.703 ms | nodes=2368
heuristic_lcv:
  size_16/samimsu_level253 |    150.780 ms | nodes=1805
csp_ac3:
  size_16/samimsu_level310 |    390.710 ms | nodes=1044
  size_16/samimsu_level253 |    230.576 ms | nodes=725
  size_16/samimsu_level273 |    153.184 ms | nodes=348
```

### Timeouts by Algorithm

```text
baseline           |   2 /   7 |  28.57%
csp_ac3            |   4 /   7 |  57.14%
dlx                |   0 /   7 |   0.00%
heuristic_lcv      |   6 /   7 |  85.71%
heuristic_simple   |   4 /   7 |  57.14%
```

## Size 17

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 2 | 1 | 50.00% | 1.917 | 1.917 | 5508.0 | 315.0 |
| csp_ac3 | 2 | 1 | 50.00% | 15.984 | 15.984 | 21.0 | 4.0 |
| dlx | 2 | 2 | 100.00% | 18.357 | 18.357 | 810.5 | 793.5 |
| heuristic_simple | 2 | 1 | 50.00% | 21.752 | 21.752 | 249.0 | 138.0 |
| heuristic_lcv | 2 | 1 | 50.00% | 27.118 | 27.118 | 184.0 | 106.0 |

### Average Time (ms)

```text
baseline           | ##                               |      1.917
csp_ac3            | ##################               |     15.984
dlx                | #####################            |     18.357
heuristic_simple   | #########################        |     21.752
heuristic_lcv      | ################################ |     27.118
```

### Average Nodes

```text
baseline           | ################################ |   5508.000
csp_ac3            | #                                |     21.000
dlx                | ####                             |    810.500
heuristic_simple   | #                                |    249.000
heuristic_lcv      | #                                |    184.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_17/samimsu_level213 |      1.917 ms | nodes=5508
heuristic_simple:
  size_17/samimsu_level213 |     21.752 ms | nodes=249
heuristic_lcv:
  size_17/samimsu_level213 |     27.118 ms | nodes=184
dlx:
  size_17/samimsu_level213 |     27.217 ms | nodes=1245
  size_17/samimsu_level302 |      9.497 ms | nodes=376
csp_ac3:
  size_17/samimsu_level213 |     15.984 ms | nodes=21
```

### Timeouts by Algorithm

```text
baseline           |   1 /   2 |  50.00%
csp_ac3            |   1 /   2 |  50.00%
dlx                |   0 /   2 |   0.00%
heuristic_lcv      |   1 /   2 |  50.00%
heuristic_simple   |   1 /   2 |  50.00%
```

## Size 18

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heuristic_simple | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| heuristic_lcv | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| csp_ac3 | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 4 | 4 | 100.00% | 24.105 | 5.005 | 985.5 | 967.5 |
| baseline | 4 | 1 | 25.00% | 157.362 | 157.362 | 458433.0 | 25459.0 |

### Average Time (ms)

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
dlx                | ####                             |     24.105
baseline           | ################################ |    157.362
```

### Average Nodes

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
dlx                | #                                |    985.500
baseline           | ################################ | 458433.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_18/samimsu_level229 |    157.362 ms | nodes=458433
dlx:
  size_18/samimsu_level229 |     83.086 ms | nodes=3734
  size_18/samimsu_level373 |      5.212 ms | nodes=91
  size_18/samimsu_level409 |      4.798 ms | nodes=95
```

### Timeouts by Algorithm

```text
baseline           |   3 /   4 |  75.00%
csp_ac3            |   4 /   4 | 100.00%
dlx                |   0 /   4 |   0.00%
heuristic_lcv      |   4 /   4 | 100.00%
heuristic_simple   |   4 /   4 | 100.00%
```

## Size 6

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 45 | 45 | 100.00% | 0.150 | 0.144 | 307.8 | 47.8 |
| dlx | 45 | 45 | 100.00% | 0.408 | 0.329 | 9.1 | 3.1 |
| heuristic_simple | 45 | 45 | 100.00% | 0.433 | 0.468 | 42.8 | 20.8 |
| csp_ac3 | 45 | 45 | 100.00% | 0.588 | 0.486 | 11.1 | 5.1 |
| heuristic_lcv | 45 | 45 | 100.00% | 0.603 | 0.521 | 37.7 | 17.8 |

### Average Time (ms)

```text
baseline           | #######                          |      0.150
dlx                | #####################            |      0.408
heuristic_simple   | ######################           |      0.433
csp_ac3            | ###############################  |      0.588
heuristic_lcv      | ################################ |      0.603
```

### Average Nodes

```text
baseline           | ################################ |    307.800
dlx                | #                                |      9.089
heuristic_simple   | ####                             |     42.800
csp_ac3            | #                                |     11.133
heuristic_lcv      | ###                              |     37.689
```

### Slowest Puzzles (by time)

```text
baseline:
  size_6/samimsu_level262 |      0.410 ms | nodes=855
  size_6/samimsu_level337 |      0.394 ms | nodes=843
  size_6/samimsu_level21 |      0.332 ms | nodes=699
heuristic_simple:
  size_6/samimsu_level337 |      1.067 ms | nodes=114
  size_6/samimsu_level139 |      0.930 ms | nodes=95
  size_6/samimsu_level21 |      0.806 ms | nodes=87
heuristic_lcv:
  size_6/samimsu_level337 |      1.717 ms | nodes=121
  size_6/samimsu_level377 |      1.607 ms | nodes=103
  size_6/samimsu_level10 |      1.285 ms | nodes=87
dlx:
  size_6/samimsu_level323 |      0.875 ms | nodes=7
  size_6/samimsu_level358 |      0.861 ms | nodes=10
  size_6/samimsu_level118 |      0.793 ms | nodes=6
csp_ac3:
  size_6/samimsu_level337 |      1.810 ms | nodes=31
  size_6/samimsu_level178 |      1.191 ms | nodes=20
  size_6/samimsu_level109 |      1.187 ms | nodes=25
```

### Timeouts by Algorithm

```text
baseline           |   0 /  45 |   0.00%
csp_ac3            |   0 /  45 |   0.00%
dlx                |   0 /  45 |   0.00%
heuristic_lcv      |   0 /  45 |   0.00%
heuristic_simple   |   0 /  45 |   0.00%
```

## Size 7

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 156 | 156 | 100.00% | 0.398 | 0.234 | 887.7 | 122.8 |
| dlx | 156 | 156 | 100.00% | 0.562 | 0.432 | 12.4 | 5.4 |
| heuristic_simple | 156 | 156 | 100.00% | 1.032 | 0.675 | 86.6 | 44.4 |
| heuristic_lcv | 156 | 156 | 100.00% | 1.281 | 0.908 | 65.8 | 32.4 |
| csp_ac3 | 156 | 156 | 100.00% | 1.365 | 0.860 | 18.6 | 11.6 |

### Average Time (ms)

```text
baseline           | #########                        |      0.398
dlx                | #############                    |      0.562
heuristic_simple   | ########################         |      1.032
heuristic_lcv      | ##############################   |      1.281
csp_ac3            | ################################ |      1.365
```

### Average Nodes

```text
baseline           | ################################ |    887.744
dlx                | #                                |     12.423
heuristic_simple   | ###                              |     86.583
heuristic_lcv      | ##                               |     65.763
csp_ac3            | #                                |     18.609
```

### Slowest Puzzles (by time)

```text
baseline:
  size_7/samimsu_level211 |      1.819 ms | nodes=4235
  size_7/samimsu_level8 |      1.721 ms | nodes=3871
  size_7/samimsu_level91 |      1.603 ms | nodes=3640
heuristic_simple:
  size_7/samimsu_level177 |      4.767 ms | nodes=446
  size_7/samimsu_level42 |      3.991 ms | nodes=350
  size_7/samimsu_level394 |      3.646 ms | nodes=320
heuristic_lcv:
  size_7/samimsu_level31 |      5.667 ms | nodes=326
  size_7/samimsu_level315 |      4.839 ms | nodes=272
  size_7/samimsu_level135 |      4.380 ms | nodes=265
dlx:
  size_7/samimsu_level451 |      3.498 ms | nodes=8
  size_7/samimsu_level79 |      2.327 ms | nodes=14
  size_7/samimsu_level386 |      1.340 ms | nodes=7
csp_ac3:
  size_7/samimsu_level148 |      6.773 ms | nodes=110
  size_7/samimsu_level331 |      6.062 ms | nodes=92
  size_7/samimsu_level388 |      5.561 ms | nodes=97
```

### Timeouts by Algorithm

```text
baseline           |   0 / 156 |   0.00%
csp_ac3            |   0 / 156 |   0.00%
dlx                |   0 / 156 |   0.00%
heuristic_lcv      |   0 / 156 |   0.00%
heuristic_simple   |   0 / 156 |   0.00%
```

## Size 8

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 54 | 54 | 100.00% | 0.763 | 0.641 | 14.2 | 6.2 |
| baseline | 54 | 54 | 100.00% | 2.178 | 1.007 | 5173.0 | 642.1 |
| heuristic_simple | 54 | 54 | 100.00% | 5.275 | 3.169 | 386.8 | 218.5 |
| heuristic_lcv | 54 | 54 | 100.00% | 5.650 | 2.497 | 258.9 | 141.9 |
| csp_ac3 | 54 | 54 | 100.00% | 6.308 | 2.272 | 77.1 | 69.1 |

### Average Time (ms)

```text
dlx                | ###                              |      0.763
baseline           | ###########                      |      2.178
heuristic_simple   | ##########################       |      5.275
heuristic_lcv      | ############################     |      5.650
csp_ac3            | ################################ |      6.308
```

### Average Nodes

```text
dlx                | #                                |     14.222
baseline           | ################################ |   5173.037
heuristic_simple   | ##                               |    386.778
heuristic_lcv      | #                                |    258.889
csp_ac3            | #                                |     77.056
```

### Slowest Puzzles (by time)

```text
baseline:
  size_8/samimsu_level274 |      9.414 ms | nodes=21756
  size_8/samimsu_level365 |      8.502 ms | nodes=19796
  size_8/samimsu_level22 |      6.345 ms | nodes=15292
heuristic_simple:
  size_8/samimsu_level274 |     21.260 ms | nodes=1643
  size_8/samimsu_level300 |     19.342 ms | nodes=1448
  size_8/samimsu_level22 |     18.625 ms | nodes=1598
heuristic_lcv:
  size_8/samimsu_level22 |     55.284 ms | nodes=2311
  size_8/samimsu_level274 |     34.368 ms | nodes=1770
  size_8/samimsu_level441 |     32.059 ms | nodes=1805
dlx:
  size_8/samimsu_level115 |      1.557 ms | nodes=9
  size_8/samimsu_level346 |      1.465 ms | nodes=13
  size_8/samimsu_level441 |      1.379 ms | nodes=60
csp_ac3:
  size_8/samimsu_level22 |     56.681 ms | nodes=829
  size_8/samimsu_level441 |     51.823 ms | nodes=717
  size_8/samimsu_level189 |     23.890 ms | nodes=340
```

### Timeouts by Algorithm

```text
baseline           |   0 /  54 |   0.00%
csp_ac3            |   0 /  54 |   0.00%
dlx                |   0 /  54 |   0.00%
heuristic_lcv      |   0 /  54 |   0.00%
heuristic_simple   |   0 /  54 |   0.00%
```

## Size 9

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 49 | 49 | 100.00% | 1.117 | 1.060 | 25.4 | 16.4 |
| baseline | 49 | 49 | 100.00% | 6.021 | 3.649 | 14920.2 | 1652.8 |
| heuristic_simple | 49 | 49 | 100.00% | 16.395 | 11.034 | 1009.6 | 581.4 |
| heuristic_lcv | 49 | 49 | 100.00% | 17.065 | 4.543 | 685.8 | 389.4 |
| csp_ac3 | 49 | 49 | 100.00% | 24.013 | 6.506 | 241.4 | 232.4 |

### Average Time (ms)

```text
dlx                | #                                |      1.117
baseline           | ########                         |      6.021
heuristic_simple   | #####################            |     16.395
heuristic_lcv      | ######################           |     17.065
csp_ac3            | ################################ |     24.013
```

### Average Nodes

```text
dlx                | #                                |     25.429
baseline           | ################################ |  14920.163
heuristic_simple   | ##                               |   1009.551
heuristic_lcv      | #                                |    685.755
csp_ac3            | #                                |    241.388
```

### Slowest Puzzles (by time)

```text
baseline:
  size_9/samimsu_level280 |     28.936 ms | nodes=71199
  size_9/samimsu_level352 |     24.403 ms | nodes=60201
  size_9/samimsu_level55 |     18.697 ms | nodes=46278
heuristic_simple:
  size_9/samimsu_level55 |     70.098 ms | nodes=4756
  size_9/samimsu_level208 |     64.800 ms | nodes=4022
  size_9/samimsu_level352 |     60.031 ms | nodes=4038
heuristic_lcv:
  size_9/samimsu_level352 |     86.030 ms | nodes=3833
  size_9/samimsu_level428 |     78.573 ms | nodes=3340
  size_9/samimsu_level94 |     56.907 ms | nodes=2302
dlx:
  size_9/samimsu_level352 |      2.343 ms | nodes=133
  size_9/samimsu_level318 |      2.276 ms | nodes=92
  size_9/samimsu_level437 |      2.065 ms | nodes=111
csp_ac3:
  size_9/samimsu_level428 |    130.795 ms | nodes=1489
  size_9/samimsu_level352 |    126.233 ms | nodes=1403
  size_9/samimsu_level321 |     86.408 ms | nodes=858
```

### Timeouts by Algorithm

```text
baseline           |   0 /  49 |   0.00%
csp_ac3            |   0 /  49 |   0.00%
dlx                |   0 /  49 |   0.00%
heuristic_lcv      |   0 /  49 |   0.00%
heuristic_simple   |   0 /  49 |   0.00%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.