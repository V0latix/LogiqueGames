# Queens Benchmark Report (Recursive)

- Generated: 2026-01-27 23:48:13
- Dataset root: `data/imported/queens/samimsu_by_size`
- Algorithms: baseline, dlx, heuristic_lcv, heuristic_simple
- Time limit: 0.5s

## Global Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 473 | 473 | 100.00% | 1.763 | 0.799 | 58.8 | 49.9 |
| baseline | 473 | 448 | 94.71% | 22.789 | 0.741 | 61714.7 | 5390.8 |
| heuristic_lcv | 473 | 420 | 88.79% | 26.615 | 1.704 | 827.2 | 454.7 |
| heuristic_simple | 473 | 428 | 90.49% | 31.392 | 1.823 | 1444.3 | 803.4 |

## Size 10

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 38 | 38 | 100.00% | 1.177 | 0.904 | 25.7 | 15.7 |
| baseline | 38 | 38 | 100.00% | 42.978 | 17.794 | 113921.1 | 11386.6 |
| heuristic_simple | 38 | 36 | 94.74% | 53.181 | 26.474 | 2933.9 | 1528.5 |
| heuristic_lcv | 38 | 36 | 94.74% | 62.787 | 11.063 | 2366.2 | 1181.2 |

### Average Time (ms)

```text
dlx                | #                                |      1.177
baseline           | #####################            |     42.978
heuristic_simple   | ###########################      |     53.181
heuristic_lcv      | ################################ |     62.787
```

### Average Nodes

```text
dlx                | #                                |     25.684
baseline           | ################################ | 113921.053
heuristic_simple   | #                                |   2933.917
heuristic_lcv      | #                                |   2366.167
```

### Slowest Puzzles (by time)

```text
baseline:
  size_10/samimsu_level290 |    249.832 ms | nodes=658955
  size_10/samimsu_level164 |    224.402 ms | nodes=613435
  size_10/samimsu_level232 |    188.395 ms | nodes=494225
heuristic_simple:
  size_10/samimsu_level190 |    352.134 ms | nodes=21293
  size_10/samimsu_level224 |    213.725 ms | nodes=14777
  size_10/samimsu_level19 |    188.928 ms | nodes=11115
heuristic_lcv:
  size_10/samimsu_level224 |    416.681 ms | nodes=18060
  size_10/samimsu_level190 |    344.332 ms | nodes=13917
  size_10/samimsu_level191 |    247.137 ms | nodes=9884
dlx:
  size_10/samimsu_level190 |      2.775 ms | nodes=194
  size_10/samimsu_level164 |      2.655 ms | nodes=44
  size_10/samimsu_level201 |      2.387 ms | nodes=38
```

### Timeouts by Algorithm

```text
baseline           |   0 /  38 |   0.00%
dlx                |   0 /  38 |   0.00%
heuristic_lcv      |   2 /  38 |   5.26%
heuristic_simple   |   2 /  38 |   5.26%
```

## Size 11

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 81 | 81 | 100.00% | 1.803 | 1.229 | 51.9 | 40.9 |
| baseline | 81 | 72 | 88.89% | 71.127 | 29.129 | 189832.7 | 17251.5 |
| heuristic_lcv | 81 | 67 | 82.72% | 83.399 | 33.694 | 2453.3 | 1385.4 |
| heuristic_simple | 81 | 69 | 85.19% | 117.162 | 71.781 | 5407.2 | 3056.7 |

### Average Time (ms)

```text
dlx                | #                                |      1.803
baseline           | ###################              |     71.127
heuristic_lcv      | ######################           |     83.399
heuristic_simple   | ################################ |    117.162
```

### Average Nodes

```text
dlx                | #                                |     51.889
baseline           | ################################ | 189832.653
heuristic_lcv      | #                                |   2453.299
heuristic_simple   | #                                |   5407.246
```

### Slowest Puzzles (by time)

```text
baseline:
  size_11/samimsu_level384 |    307.166 ms | nodes=829807
  size_11/samimsu_level294 |    281.317 ms | nodes=756525
  size_11/samimsu_level40 |    280.957 ms | nodes=749958
heuristic_simple:
  size_11/samimsu_level20 |    452.481 ms | nodes=21263
  size_11/samimsu_level181 |    449.336 ms | nodes=25894
  size_11/samimsu_level76 |    435.476 ms | nodes=23880
heuristic_lcv:
  size_11/samimsu_level187 |    486.868 ms | nodes=14863
  size_11/samimsu_level276 |    475.238 ms | nodes=15151
  size_11/samimsu_level317 |    410.690 ms | nodes=10493
dlx:
  size_11/samimsu_level234 |     10.149 ms | nodes=690
  size_11/samimsu_level256 |      5.137 ms | nodes=20
  size_11/samimsu_level295 |      4.875 ms | nodes=44
```

### Timeouts by Algorithm

```text
baseline           |   9 /  81 |  11.11%
dlx                |   0 /  81 |   0.00%
heuristic_lcv      |  14 /  81 |  17.28%
heuristic_simple   |  12 /  81 |  14.81%
```

## Size 12

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heuristic_lcv | 5 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 5 | 5 | 100.00% | 1.881 | 1.990 | 40.8 | 28.8 |
| baseline | 5 | 3 | 60.00% | 201.307 | 135.548 | 558354.0 | 46523.0 |
| heuristic_simple | 5 | 1 | 20.00% | 365.123 | 365.123 | 17702.0 | 9417.0 |

### Average Time (ms)

```text
heuristic_lcv      | #                                |      0.000
dlx                | #                                |      1.881
baseline           | #################                |    201.307
heuristic_simple   | ################################ |    365.123
```

### Average Nodes

```text
heuristic_lcv      | #                                |      0.000
dlx                | #                                |     40.800
baseline           | ################################ | 558354.000
heuristic_simple   | #                                |  17702.000
```

### Slowest Puzzles (by time)

```text
dlx:
  size_12/samimsu_level223 |      2.175 ms | nodes=32
  size_12/samimsu_level194 |      2.033 ms | nodes=28
  size_12/samimsu_level303 |      1.990 ms | nodes=64
baseline:
  size_12/samimsu_level223 |    360.371 ms | nodes=1001034
  size_12/samimsu_level204 |    135.548 ms | nodes=381834
  size_12/samimsu_level202 |    108.002 ms | nodes=292194
heuristic_simple:
  size_12/samimsu_level202 |    365.123 ms | nodes=17702
```

### Timeouts by Algorithm

```text
baseline           |   2 /   5 |  40.00%
dlx                |   0 /   5 |   0.00%
heuristic_lcv      |   5 /   5 | 100.00%
heuristic_simple   |   4 /   5 |  80.00%
```

## Size 13

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 14 | 14 | 100.00% | 2.896 | 2.042 | 84.0 | 71.0 |
| baseline | 14 | 12 | 85.71% | 45.940 | 5.721 | 128328.4 | 9864.4 |
| heuristic_simple | 14 | 8 | 57.14% | 72.876 | 22.408 | 1929.4 | 1112.2 |
| heuristic_lcv | 14 | 7 | 50.00% | 163.788 | 68.813 | 3747.3 | 2277.9 |

### Average Time (ms)

```text
dlx                | #                                |      2.896
baseline           | ########                         |     45.940
heuristic_simple   | ##############                   |     72.876
heuristic_lcv      | ################################ |    163.788
```

### Average Nodes

```text
dlx                | #                                |     84.000
baseline           | ################################ | 128328.417
heuristic_simple   | #                                |   1929.375
heuristic_lcv      | #                                |   3747.286
```

### Slowest Puzzles (by time)

```text
baseline:
  size_13/samimsu_level278 |    178.172 ms | nodes=491244
  size_13/samimsu_level244 |    148.703 ms | nodes=416741
  size_13/samimsu_level237 |    142.533 ms | nodes=406874
heuristic_simple:
  size_13/samimsu_level221 |    382.506 ms | nodes=10056
  size_13/samimsu_level219 |     82.368 ms | nodes=2082
  size_13/samimsu_level305 |     54.469 ms | nodes=1414
heuristic_lcv:
  size_13/samimsu_level248 |    498.831 ms | nodes=12178
  size_13/samimsu_level279 |    349.272 ms | nodes=8227
  size_13/samimsu_level305 |    155.725 ms | nodes=2688
dlx:
  size_13/samimsu_level237 |      8.940 ms | nodes=373
  size_13/samimsu_level195 |      5.672 ms | nodes=284
  size_13/samimsu_level226 |      3.338 ms | nodes=104
```

### Timeouts by Algorithm

```text
baseline           |   2 /  14 |  14.29%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |   7 /  14 |  50.00%
heuristic_simple   |   6 /  14 |  42.86%
```

## Size 14

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 4 | 4 | 100.00% | 3.562 | 2.631 | 111.2 | 97.2 |
| heuristic_lcv | 4 | 1 | 25.00% | 6.763 | 6.763 | 81.0 | 38.0 |
| baseline | 4 | 1 | 25.00% | 12.992 | 12.992 | 35889.0 | 2556.0 |
| heuristic_simple | 4 | 1 | 25.00% | 76.568 | 76.568 | 1695.0 | 1059.0 |

### Average Time (ms)

```text
dlx                | #                                |      3.562
heuristic_lcv      | ##                               |      6.763
baseline           | #####                            |     12.992
heuristic_simple   | ################################ |     76.568
```

### Average Nodes

```text
dlx                | #                                |    111.250
heuristic_lcv      | #                                |     81.000
baseline           | ################################ |  35889.000
heuristic_simple   | #                                |   1695.000
```

### Slowest Puzzles (by time)

```text
dlx:
  size_14/samimsu_level212 |      7.075 ms | nodes=335
  size_14/samimsu_level296 |      3.097 ms | nodes=75
  size_14/samimsu_level228 |      2.165 ms | nodes=21
baseline:
  size_14/samimsu_level296 |     12.992 ms | nodes=35889
heuristic_simple:
  size_14/samimsu_level296 |     76.568 ms | nodes=1695
heuristic_lcv:
  size_14/samimsu_level296 |      6.763 ms | nodes=81
```

### Timeouts by Algorithm

```text
baseline           |   3 /   4 |  75.00%
dlx                |   0 /   4 |   0.00%
heuristic_lcv      |   3 /   4 |  75.00%
heuristic_simple   |   3 /   4 |  75.00%
```

## Size 15

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 14 | 14 | 100.00% | 8.976 | 3.135 | 365.0 | 350.0 |
| heuristic_simple | 14 | 4 | 28.57% | 45.967 | 34.931 | 777.5 | 436.2 |
| baseline | 14 | 11 | 78.57% | 143.122 | 104.266 | 410179.1 | 27337.3 |
| heuristic_lcv | 14 | 3 | 21.43% | 228.689 | 208.751 | 3349.3 | 1935.7 |

### Average Time (ms)

```text
dlx                | #                                |      8.976
heuristic_simple   | ######                           |     45.967
baseline           | ####################             |    143.122
heuristic_lcv      | ################################ |    228.689
```

### Average Nodes

```text
dlx                | #                                |    365.000
heuristic_simple   | #                                |    777.500
baseline           | ################################ | 410179.091
heuristic_lcv      | #                                |   3349.333
```

### Slowest Puzzles (by time)

```text
baseline:
  size_15/samimsu_level214 |    419.164 ms | nodes=1171635
  size_15/samimsu_level205 |    370.243 ms | nodes=1078680
  size_15/samimsu_level270 |    255.190 ms | nodes=742395
dlx:
  size_15/samimsu_level205 |     65.255 ms | nodes=3110
  size_15/samimsu_level263 |     15.377 ms | nodes=668
  size_15/samimsu_level306 |      9.016 ms | nodes=504
heuristic_simple:
  size_15/samimsu_level230 |    107.561 ms | nodes=1597
  size_15/samimsu_level271 |     42.870 ms | nodes=690
  size_15/samimsu_level297 |     26.993 ms | nodes=676
heuristic_lcv:
  size_15/samimsu_level230 |    421.416 ms | nodes=5365
  size_15/samimsu_level371 |    208.751 ms | nodes=4062
  size_15/samimsu_level271 |     55.902 ms | nodes=621
```

### Timeouts by Algorithm

```text
baseline           |   3 /  14 |  21.43%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |  11 /  14 |  78.57%
heuristic_simple   |  10 /  14 |  71.43%
```

## Size 16

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 7 | 5 | 71.43% | 17.485 | 12.850 | 52331.2 | 3262.2 |
| dlx | 7 | 7 | 100.00% | 17.530 | 10.462 | 825.4 | 809.4 |
| heuristic_lcv | 7 | 1 | 14.29% | 147.817 | 147.817 | 1805.0 | 1144.0 |
| heuristic_simple | 7 | 4 | 57.14% | 242.108 | 168.916 | 3866.8 | 2131.0 |

### Average Time (ms)

```text
baseline           | ##                               |     17.485
dlx                | ##                               |     17.530
heuristic_lcv      | ###################              |    147.817
heuristic_simple   | ################################ |    242.108
```

### Average Nodes

```text
baseline           | ################################ |  52331.200
dlx                | #                                |    825.429
heuristic_lcv      | #                                |   1805.000
heuristic_simple   | ##                               |   3866.750
```

### Slowest Puzzles (by time)

```text
dlx:
  size_16/samimsu_level273 |     65.494 ms | nodes=3803
  size_16/samimsu_level258 |     21.939 ms | nodes=906
  size_16/samimsu_level253 |     11.178 ms | nodes=357
baseline:
  size_16/samimsu_level273 |     44.781 ms | nodes=134056
  size_16/samimsu_level258 |     21.674 ms | nodes=65208
  size_16/samimsu_level310 |     12.850 ms | nodes=38584
heuristic_simple:
  size_16/samimsu_level273 |    493.205 ms | nodes=7147
  size_16/samimsu_level258 |    171.772 ms | nodes=2608
  size_16/samimsu_level253 |    166.059 ms | nodes=3344
heuristic_lcv:
  size_16/samimsu_level253 |    147.817 ms | nodes=1805
```

### Timeouts by Algorithm

```text
baseline           |   2 /   7 |  28.57%
dlx                |   0 /   7 |   0.00%
heuristic_lcv      |   6 /   7 |  85.71%
heuristic_simple   |   3 /   7 |  42.86%
```

## Size 17

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 2 | 1 | 50.00% | 1.883 | 1.883 | 5508.0 | 315.0 |
| dlx | 2 | 2 | 100.00% | 17.762 | 17.762 | 810.5 | 793.5 |
| heuristic_simple | 2 | 1 | 50.00% | 20.831 | 20.831 | 249.0 | 138.0 |
| heuristic_lcv | 2 | 1 | 50.00% | 26.317 | 26.317 | 184.0 | 106.0 |

### Average Time (ms)

```text
baseline           | ##                               |      1.883
dlx                | #####################            |     17.762
heuristic_simple   | #########################        |     20.831
heuristic_lcv      | ################################ |     26.317
```

### Average Nodes

```text
baseline           | ################################ |   5508.000
dlx                | ####                             |    810.500
heuristic_simple   | #                                |    249.000
heuristic_lcv      | #                                |    184.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_17/samimsu_level213 |      1.883 ms | nodes=5508
heuristic_simple:
  size_17/samimsu_level213 |     20.831 ms | nodes=249
heuristic_lcv:
  size_17/samimsu_level213 |     26.317 ms | nodes=184
dlx:
  size_17/samimsu_level213 |     27.121 ms | nodes=1245
  size_17/samimsu_level302 |      8.403 ms | nodes=376
```

### Timeouts by Algorithm

```text
baseline           |   1 /   2 |  50.00%
dlx                |   0 /   2 |   0.00%
heuristic_lcv      |   1 /   2 |  50.00%
heuristic_simple   |   1 /   2 |  50.00%
```

## Size 18

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heuristic_simple | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| heuristic_lcv | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 4 | 4 | 100.00% | 24.346 | 5.165 | 985.5 | 967.5 |
| baseline | 4 | 1 | 25.00% | 153.268 | 153.268 | 458433.0 | 25459.0 |

### Average Time (ms)

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
dlx                | #####                            |     24.346
baseline           | ################################ |    153.268
```

### Average Nodes

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
dlx                | #                                |    985.500
baseline           | ################################ | 458433.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_18/samimsu_level229 |    153.268 ms | nodes=458433
dlx:
  size_18/samimsu_level229 |     83.853 ms | nodes=3734
  size_18/samimsu_level409 |      5.220 ms | nodes=95
  size_18/samimsu_level373 |      5.110 ms | nodes=91
```

### Timeouts by Algorithm

```text
baseline           |   3 /   4 |  75.00%
dlx                |   0 /   4 |   0.00%
heuristic_lcv      |   4 /   4 | 100.00%
heuristic_simple   |   4 /   4 | 100.00%
```

## Size 6

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 45 | 45 | 100.00% | 0.147 | 0.142 | 307.8 | 47.8 |
| dlx | 45 | 45 | 100.00% | 0.403 | 0.321 | 9.1 | 3.1 |
| heuristic_simple | 45 | 45 | 100.00% | 0.425 | 0.428 | 42.8 | 20.8 |
| heuristic_lcv | 45 | 45 | 100.00% | 0.597 | 0.545 | 37.7 | 17.8 |

### Average Time (ms)

```text
baseline           | #######                          |      0.147
dlx                | #####################            |      0.403
heuristic_simple   | ######################           |      0.425
heuristic_lcv      | ################################ |      0.597
```

### Average Nodes

```text
baseline           | ################################ |    307.800
dlx                | #                                |      9.089
heuristic_simple   | ####                             |     42.800
heuristic_lcv      | ###                              |     37.689
```

### Slowest Puzzles (by time)

```text
baseline:
  size_6/samimsu_level262 |      0.398 ms | nodes=855
  size_6/samimsu_level337 |      0.385 ms | nodes=843
  size_6/samimsu_level21 |      0.326 ms | nodes=699
heuristic_simple:
  size_6/samimsu_level21 |      1.216 ms | nodes=87
  size_6/samimsu_level337 |      1.040 ms | nodes=114
  size_6/samimsu_level139 |      0.908 ms | nodes=95
heuristic_lcv:
  size_6/samimsu_level337 |      1.702 ms | nodes=121
  size_6/samimsu_level377 |      1.417 ms | nodes=103
  size_6/samimsu_level10 |      1.278 ms | nodes=87
dlx:
  size_6/samimsu_level363 |      0.916 ms | nodes=12
  size_6/samimsu_level425 |      0.829 ms | nodes=6
  size_6/samimsu_level299 |      0.786 ms | nodes=17
```

### Timeouts by Algorithm

```text
baseline           |   0 /  45 |   0.00%
dlx                |   0 /  45 |   0.00%
heuristic_lcv      |   0 /  45 |   0.00%
heuristic_simple   |   0 /  45 |   0.00%
```

## Size 7

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 156 | 156 | 100.00% | 0.387 | 0.229 | 887.7 | 122.8 |
| dlx | 156 | 156 | 100.00% | 0.552 | 0.426 | 12.4 | 5.4 |
| heuristic_simple | 156 | 156 | 100.00% | 1.030 | 0.740 | 86.6 | 44.4 |
| heuristic_lcv | 156 | 156 | 100.00% | 1.263 | 0.930 | 65.8 | 32.4 |

### Average Time (ms)

```text
baseline           | #########                        |      0.387
dlx                | #############                    |      0.552
heuristic_simple   | ##########################       |      1.030
heuristic_lcv      | ################################ |      1.263
```

### Average Nodes

```text
baseline           | ################################ |    887.744
dlx                | #                                |     12.423
heuristic_simple   | ###                              |     86.583
heuristic_lcv      | ##                               |     65.763
```

### Slowest Puzzles (by time)

```text
baseline:
  size_7/samimsu_level211 |      1.793 ms | nodes=4235
  size_7/samimsu_level8 |      1.665 ms | nodes=3871
  size_7/samimsu_level91 |      1.584 ms | nodes=3640
heuristic_simple:
  size_7/samimsu_level177 |      4.679 ms | nodes=446
  size_7/samimsu_level42 |      3.811 ms | nodes=350
  size_7/samimsu_level394 |      3.651 ms | nodes=320
heuristic_lcv:
  size_7/samimsu_level31 |      5.314 ms | nodes=326
  size_7/samimsu_level315 |      4.746 ms | nodes=272
  size_7/samimsu_level135 |      4.290 ms | nodes=265
dlx:
  size_7/samimsu_level416 |      1.347 ms | nodes=80
  size_7/samimsu_level102 |      1.317 ms | nodes=36
  size_7/samimsu_level129 |      1.300 ms | nodes=39
```

### Timeouts by Algorithm

```text
baseline           |   0 / 156 |   0.00%
dlx                |   0 / 156 |   0.00%
heuristic_lcv      |   0 / 156 |   0.00%
heuristic_simple   |   0 / 156 |   0.00%
```

## Size 8

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 54 | 54 | 100.00% | 0.757 | 0.576 | 14.2 | 6.2 |
| baseline | 54 | 54 | 100.00% | 2.122 | 0.983 | 5173.0 | 642.1 |
| heuristic_simple | 54 | 54 | 100.00% | 5.086 | 2.954 | 386.8 | 218.5 |
| heuristic_lcv | 54 | 54 | 100.00% | 5.195 | 2.232 | 258.9 | 141.9 |

### Average Time (ms)

```text
dlx                | ####                             |      0.757
baseline           | #############                    |      2.122
heuristic_simple   | ###############################  |      5.086
heuristic_lcv      | ################################ |      5.195
```

### Average Nodes

```text
dlx                | #                                |     14.222
baseline           | ################################ |   5173.037
heuristic_simple   | ##                               |    386.778
heuristic_lcv      | #                                |    258.889
```

### Slowest Puzzles (by time)

```text
baseline:
  size_8/samimsu_level274 |      8.922 ms | nodes=21756
  size_8/samimsu_level365 |      8.180 ms | nodes=19796
  size_8/samimsu_level22 |      6.194 ms | nodes=15292
heuristic_simple:
  size_8/samimsu_level274 |     20.684 ms | nodes=1643
  size_8/samimsu_level300 |     18.395 ms | nodes=1448
  size_8/samimsu_level22 |     17.812 ms | nodes=1598
heuristic_lcv:
  size_8/samimsu_level22 |     38.933 ms | nodes=2311
  size_8/samimsu_level274 |     33.251 ms | nodes=1770
  size_8/samimsu_level441 |     31.333 ms | nodes=1805
dlx:
  size_8/samimsu_level117 |      3.432 ms | nodes=8
  size_8/samimsu_level24 |      2.077 ms | nodes=8
  size_8/samimsu_level441 |      1.455 ms | nodes=60
```

### Timeouts by Algorithm

```text
baseline           |   0 /  54 |   0.00%
dlx                |   0 /  54 |   0.00%
heuristic_lcv      |   0 /  54 |   0.00%
heuristic_simple   |   0 /  54 |   0.00%
```

## Size 9

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 49 | 49 | 100.00% | 1.072 | 0.993 | 25.4 | 16.4 |
| baseline | 49 | 49 | 100.00% | 5.891 | 3.695 | 14920.2 | 1652.8 |
| heuristic_simple | 49 | 49 | 100.00% | 16.016 | 10.630 | 1009.6 | 581.4 |
| heuristic_lcv | 49 | 49 | 100.00% | 16.575 | 4.496 | 685.8 | 389.4 |

### Average Time (ms)

```text
dlx                | ##                               |      1.072
baseline           | ###########                      |      5.891
heuristic_simple   | ##############################   |     16.016
heuristic_lcv      | ################################ |     16.575
```

### Average Nodes

```text
dlx                | #                                |     25.429
baseline           | ################################ |  14920.163
heuristic_simple   | ##                               |   1009.551
heuristic_lcv      | #                                |    685.755
```

### Slowest Puzzles (by time)

```text
baseline:
  size_9/samimsu_level280 |     28.009 ms | nodes=71199
  size_9/samimsu_level352 |     23.891 ms | nodes=60201
  size_9/samimsu_level55 |     18.369 ms | nodes=46278
heuristic_simple:
  size_9/samimsu_level55 |     69.269 ms | nodes=4756
  size_9/samimsu_level208 |     62.473 ms | nodes=4022
  size_9/samimsu_level352 |     58.840 ms | nodes=4038
heuristic_lcv:
  size_9/samimsu_level352 |     85.089 ms | nodes=3833
  size_9/samimsu_level428 |     77.673 ms | nodes=3340
  size_9/samimsu_level94 |     56.633 ms | nodes=2302
dlx:
  size_9/samimsu_level352 |      2.829 ms | nodes=133
  size_9/samimsu_level437 |      2.492 ms | nodes=111
  size_9/samimsu_level423 |      1.793 ms | nodes=35
```

### Timeouts by Algorithm

```text
baseline           |   0 /  49 |   0.00%
dlx                |   0 /  49 |   0.00%
heuristic_lcv      |   0 /  49 |   0.00%
heuristic_simple   |   0 /  49 |   0.00%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.