# Queens Benchmark Report (Recursive)

- Generated: 2026-01-28 00:35:28
- Dataset root: `data/imported/queens/samimsu_by_size`
- Algorithms: baseline, csp_ac3, dlx, heuristic_lcv, heuristic_simple, min_conflicts
- Time limit: 0.5s

## Global Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 473 | 473 | 100.00% | 1.792 | 0.871 | 58.8 | 49.9 |
| baseline | 473 | 448 | 94.71% | 23.329 | 0.784 | 61714.7 | 5390.8 |
| heuristic_lcv | 473 | 419 | 88.58% | 26.044 | 1.764 | 800.1 | 437.0 |
| csp_ac3 | 473 | 431 | 91.12% | 26.275 | 1.929 | 173.6 | 165.1 |
| heuristic_simple | 473 | 427 | 90.27% | 31.092 | 1.842 | 1431.0 | 795.9 |
| min_conflicts | 473 | 62 | 13.11% | 209.290 | 208.006 | 14860.7 | 3.0 |

## Size 10

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 38 | 38 | 100.00% | 1.280 | 0.945 | 25.7 | 15.7 |
| baseline | 38 | 38 | 100.00% | 44.735 | 18.488 | 113921.1 | 11386.6 |
| csp_ac3 | 38 | 38 | 100.00% | 51.674 | 5.496 | 444.7 | 434.7 |
| heuristic_simple | 38 | 36 | 94.74% | 55.000 | 27.547 | 2933.9 | 1528.5 |
| heuristic_lcv | 38 | 36 | 94.74% | 65.034 | 11.386 | 2366.2 | 1181.2 |
| min_conflicts | 38 | 2 | 5.26% | 131.019 | 131.019 | 5028.0 | 1.0 |

### Average Time (ms)

```text
dlx                | #                                |      1.280
baseline           | ##########                       |     44.735
csp_ac3            | ############                     |     51.674
heuristic_simple   | #############                    |     55.000
heuristic_lcv      | ###############                  |     65.034
min_conflicts      | ################################ |    131.019
```

### Average Nodes

```text
dlx                | #                                |     25.684
baseline           | ################################ | 113921.053
csp_ac3            | #                                |    444.658
heuristic_simple   | #                                |   2933.917
heuristic_lcv      | #                                |   2366.167
min_conflicts      | #                                |   5028.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_10/samimsu_level290 |    268.669 ms | nodes=658955
  size_10/samimsu_level164 |    235.291 ms | nodes=613435
  size_10/samimsu_level232 |    192.215 ms | nodes=494225
heuristic_simple:
  size_10/samimsu_level190 |    367.066 ms | nodes=21293
  size_10/samimsu_level224 |    226.918 ms | nodes=14777
  size_10/samimsu_level19 |    194.721 ms | nodes=11115
heuristic_lcv:
  size_10/samimsu_level224 |    430.957 ms | nodes=18060
  size_10/samimsu_level190 |    361.605 ms | nodes=13917
  size_10/samimsu_level191 |    252.636 ms | nodes=9884
dlx:
  size_10/samimsu_level190 |      2.942 ms | nodes=194
  size_10/samimsu_level201 |      2.694 ms | nodes=38
  size_10/samimsu_level328 |      2.542 ms | nodes=64
csp_ac3:
  size_10/samimsu_level190 |    463.818 ms | nodes=4257
  size_10/samimsu_level191 |    358.763 ms | nodes=2991
  size_10/samimsu_level164 |    351.792 ms | nodes=3509
min_conflicts:
  size_10/samimsu_level13 |    261.333 ms | nodes=10031
  size_10/samimsu_level108 |      0.704 ms | nodes=25
```

### Timeouts by Algorithm

```text
baseline           |   0 /  38 |   0.00%
csp_ac3            |   0 /  38 |   0.00%
dlx                |   0 /  38 |   0.00%
heuristic_lcv      |   2 /  38 |   5.26%
heuristic_simple   |   2 /  38 |   5.26%
min_conflicts      |  36 /  38 |  94.74%
```

## Size 11

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 81 | 81 | 100.00% | 1.666 | 1.177 | 51.9 | 40.9 |
| csp_ac3 | 81 | 70 | 86.42% | 63.029 | 16.391 | 412.0 | 401.0 |
| baseline | 81 | 72 | 88.89% | 72.547 | 29.819 | 189832.7 | 17251.5 |
| heuristic_lcv | 81 | 67 | 82.72% | 84.710 | 35.055 | 2453.3 | 1385.4 |
| heuristic_simple | 81 | 69 | 85.19% | 119.807 | 73.005 | 5407.2 | 3056.7 |
| min_conflicts | 81 | 4 | 4.94% | 235.156 | 233.886 | 7558.5 | 1.5 |

### Average Time (ms)

```text
dlx                | #                                |      1.666
csp_ac3            | ########                         |     63.029
baseline           | #########                        |     72.547
heuristic_lcv      | ###########                      |     84.710
heuristic_simple   | ################                 |    119.807
min_conflicts      | ################################ |    235.156
```

### Average Nodes

```text
dlx                | #                                |     51.889
csp_ac3            | #                                |    412.000
baseline           | ################################ | 189832.653
heuristic_lcv      | #                                |   2453.299
heuristic_simple   | #                                |   5407.246
min_conflicts      | #                                |   7558.500
```

### Slowest Puzzles (by time)

```text
baseline:
  size_11/samimsu_level384 |    314.977 ms | nodes=829807
  size_11/samimsu_level294 |    288.894 ms | nodes=756525
  size_11/samimsu_level40 |    287.669 ms | nodes=749958
heuristic_simple:
  size_11/samimsu_level20 |    455.002 ms | nodes=21263
  size_11/samimsu_level76 |    447.127 ms | nodes=23880
  size_11/samimsu_level181 |    446.153 ms | nodes=25894
heuristic_lcv:
  size_11/samimsu_level187 |    494.523 ms | nodes=14863
  size_11/samimsu_level276 |    479.422 ms | nodes=15151
  size_11/samimsu_level317 |    418.333 ms | nodes=10493
dlx:
  size_11/samimsu_level234 |     10.111 ms | nodes=690
  size_11/samimsu_level276 |      4.740 ms | nodes=245
  size_11/samimsu_level307 |      4.644 ms | nodes=194
csp_ac3:
  size_11/samimsu_level142 |    471.105 ms | nodes=3275
  size_11/samimsu_level401 |    326.877 ms | nodes=2304
  size_11/samimsu_level389 |    245.196 ms | nodes=1680
min_conflicts:
  size_11/samimsu_level7 |    472.625 ms | nodes=15180
  size_11/samimsu_level155 |    467.338 ms | nodes=15038
  size_11/samimsu_level11 |      0.434 ms | nodes=11
```

### Timeouts by Algorithm

```text
baseline           |   9 /  81 |  11.11%
csp_ac3            |  11 /  81 |  13.58%
dlx                |   0 /  81 |   0.00%
heuristic_lcv      |  14 /  81 |  17.28%
heuristic_simple   |  12 /  81 |  14.81%
min_conflicts      |  77 /  81 |  95.06%
```

## Size 12

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heuristic_lcv | 5 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| csp_ac3 | 5 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| min_conflicts | 5 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 5 | 5 | 100.00% | 1.821 | 1.735 | 40.8 | 28.8 |
| baseline | 5 | 3 | 60.00% | 208.604 | 139.460 | 558354.0 | 46523.0 |
| heuristic_simple | 5 | 1 | 20.00% | 376.104 | 376.104 | 17702.0 | 9417.0 |

### Average Time (ms)

```text
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
min_conflicts      | #                                |      0.000
dlx                | #                                |      1.821
baseline           | #################                |    208.604
heuristic_simple   | ################################ |    376.104
```

### Average Nodes

```text
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
min_conflicts      | #                                |      0.000
dlx                | #                                |     40.800
baseline           | ################################ | 558354.000
heuristic_simple   | #                                |  17702.000
```

### Slowest Puzzles (by time)

```text
dlx:
  size_12/samimsu_level303 |      2.167 ms | nodes=64
  size_12/samimsu_level204 |      2.112 ms | nodes=64
  size_12/samimsu_level223 |      1.735 ms | nodes=32
baseline:
  size_12/samimsu_level223 |    374.779 ms | nodes=1001034
  size_12/samimsu_level204 |    139.460 ms | nodes=381834
  size_12/samimsu_level202 |    111.572 ms | nodes=292194
heuristic_simple:
  size_12/samimsu_level202 |    376.104 ms | nodes=17702
```

### Timeouts by Algorithm

```text
baseline           |   2 /   5 |  40.00%
csp_ac3            |   5 /   5 | 100.00%
dlx                |   0 /   5 |   0.00%
heuristic_lcv      |   5 /   5 | 100.00%
heuristic_simple   |   4 /   5 |  80.00%
min_conflicts      |   5 /   5 | 100.00%
```

## Size 13

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| min_conflicts | 14 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 14 | 14 | 100.00% | 2.936 | 2.141 | 84.0 | 71.0 |
| baseline | 14 | 12 | 85.71% | 46.816 | 5.989 | 128328.4 | 9864.4 |
| heuristic_simple | 14 | 8 | 57.14% | 74.911 | 22.823 | 1929.4 | 1112.2 |
| csp_ac3 | 14 | 7 | 50.00% | 84.456 | 55.480 | 332.1 | 319.1 |
| heuristic_lcv | 14 | 6 | 42.86% | 109.336 | 64.254 | 2342.2 | 1346.3 |

### Average Time (ms)

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |      2.936
baseline           | #############                    |     46.816
heuristic_simple   | #####################            |     74.911
csp_ac3            | ########################         |     84.456
heuristic_lcv      | ################################ |    109.336
```

### Average Nodes

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |     84.000
baseline           | ################################ | 128328.417
heuristic_simple   | #                                |   1929.375
csp_ac3            | #                                |    332.143
heuristic_lcv      | #                                |   2342.167
```

### Slowest Puzzles (by time)

```text
baseline:
  size_13/samimsu_level278 |    180.075 ms | nodes=491244
  size_13/samimsu_level244 |    151.139 ms | nodes=416741
  size_13/samimsu_level237 |    146.048 ms | nodes=406874
heuristic_simple:
  size_13/samimsu_level221 |    393.279 ms | nodes=10056
  size_13/samimsu_level219 |     85.246 ms | nodes=2082
  size_13/samimsu_level305 |     55.538 ms | nodes=1414
heuristic_lcv:
  size_13/samimsu_level279 |    352.328 ms | nodes=8227
  size_13/samimsu_level305 |    156.711 ms | nodes=2688
  size_13/samimsu_level195 |     71.921 ms | nodes=1759
dlx:
  size_13/samimsu_level237 |      9.180 ms | nodes=373
  size_13/samimsu_level195 |      5.661 ms | nodes=284
  size_13/samimsu_level226 |      3.643 ms | nodes=104
csp_ac3:
  size_13/samimsu_level279 |    231.486 ms | nodes=1029
  size_13/samimsu_level238 |    180.914 ms | nodes=534
  size_13/samimsu_level278 |     73.685 ms | nodes=341
```

### Timeouts by Algorithm

```text
baseline           |   2 /  14 |  14.29%
csp_ac3            |   7 /  14 |  50.00%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |   8 /  14 |  57.14%
heuristic_simple   |   6 /  14 |  42.86%
min_conflicts      |  14 /  14 | 100.00%
```

## Size 14

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| min_conflicts | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 4 | 4 | 100.00% | 3.647 | 2.683 | 111.2 | 97.2 |
| heuristic_lcv | 4 | 1 | 25.00% | 6.883 | 6.883 | 81.0 | 38.0 |
| baseline | 4 | 1 | 25.00% | 13.202 | 13.202 | 35889.0 | 2556.0 |
| csp_ac3 | 4 | 1 | 25.00% | 24.741 | 24.741 | 68.0 | 54.0 |
| heuristic_simple | 4 | 1 | 25.00% | 79.306 | 79.306 | 1695.0 | 1059.0 |

### Average Time (ms)

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |      3.647
heuristic_lcv      | ##                               |      6.883
baseline           | #####                            |     13.202
csp_ac3            | #########                        |     24.741
heuristic_simple   | ################################ |     79.306
```

### Average Nodes

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |    111.250
heuristic_lcv      | #                                |     81.000
baseline           | ################################ |  35889.000
csp_ac3            | #                                |     68.000
heuristic_simple   | #                                |   1695.000
```

### Slowest Puzzles (by time)

```text
dlx:
  size_14/samimsu_level212 |      7.263 ms | nodes=335
  size_14/samimsu_level296 |      3.141 ms | nodes=75
  size_14/samimsu_level228 |      2.225 ms | nodes=21
baseline:
  size_14/samimsu_level296 |     13.202 ms | nodes=35889
heuristic_simple:
  size_14/samimsu_level296 |     79.306 ms | nodes=1695
heuristic_lcv:
  size_14/samimsu_level296 |      6.883 ms | nodes=81
csp_ac3:
  size_14/samimsu_level296 |     24.741 ms | nodes=68
```

### Timeouts by Algorithm

```text
baseline           |   3 /   4 |  75.00%
csp_ac3            |   3 /   4 |  75.00%
dlx                |   0 /   4 |   0.00%
heuristic_lcv      |   3 /   4 |  75.00%
heuristic_simple   |   3 /   4 |  75.00%
min_conflicts      |   4 /   4 | 100.00%
```

## Size 15

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| min_conflicts | 14 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 14 | 14 | 100.00% | 8.973 | 3.167 | 365.0 | 350.0 |
| heuristic_simple | 14 | 4 | 28.57% | 47.281 | 36.136 | 777.5 | 436.2 |
| baseline | 14 | 11 | 78.57% | 145.353 | 105.599 | 410179.1 | 27337.3 |
| heuristic_lcv | 14 | 3 | 21.43% | 234.148 | 212.647 | 3349.3 | 1935.7 |
| csp_ac3 | 14 | 7 | 50.00% | 255.527 | 215.957 | 734.7 | 719.7 |

### Average Time (ms)

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |      8.973
heuristic_simple   | #####                            |     47.281
baseline           | ##################               |    145.353
heuristic_lcv      | #############################    |    234.148
csp_ac3            | ################################ |    255.527
```

### Average Nodes

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |    365.000
heuristic_simple   | #                                |    777.500
baseline           | ################################ | 410179.091
heuristic_lcv      | #                                |   3349.333
csp_ac3            | #                                |    734.714
```

### Slowest Puzzles (by time)

```text
baseline:
  size_15/samimsu_level214 |    426.229 ms | nodes=1171635
  size_15/samimsu_level205 |    375.844 ms | nodes=1078680
  size_15/samimsu_level270 |    259.218 ms | nodes=742395
dlx:
  size_15/samimsu_level205 |     67.101 ms | nodes=3110
  size_15/samimsu_level263 |     14.000 ms | nodes=668
  size_15/samimsu_level306 |      8.980 ms | nodes=504
heuristic_simple:
  size_15/samimsu_level230 |    109.812 ms | nodes=1597
  size_15/samimsu_level271 |     44.286 ms | nodes=690
  size_15/samimsu_level297 |     27.987 ms | nodes=676
heuristic_lcv:
  size_15/samimsu_level230 |    432.481 ms | nodes=5365
  size_15/samimsu_level371 |    212.647 ms | nodes=4062
  size_15/samimsu_level271 |     57.314 ms | nodes=621
csp_ac3:
  size_15/samimsu_level263 |    486.386 ms | nodes=1690
  size_15/samimsu_level245 |    443.761 ms | nodes=1384
  size_15/samimsu_level297 |    345.765 ms | nodes=682
```

### Timeouts by Algorithm

```text
baseline           |   3 /  14 |  21.43%
csp_ac3            |   7 /  14 |  50.00%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |  11 /  14 |  78.57%
heuristic_simple   |  10 /  14 |  71.43%
min_conflicts      |  14 /  14 | 100.00%
```

## Size 16

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| min_conflicts | 7 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 7 | 7 | 100.00% | 17.596 | 9.132 | 825.4 | 809.4 |
| baseline | 7 | 5 | 71.43% | 17.894 | 13.201 | 52331.2 | 3262.2 |
| heuristic_lcv | 7 | 1 | 14.29% | 151.304 | 151.304 | 1805.0 | 1144.0 |
| heuristic_simple | 7 | 3 | 42.86% | 163.949 | 171.331 | 2773.3 | 1505.7 |
| csp_ac3 | 7 | 3 | 42.86% | 257.322 | 229.965 | 705.7 | 689.7 |

### Average Time (ms)

```text
min_conflicts      | #                                |      0.000
dlx                | ##                               |     17.596
baseline           | ##                               |     17.894
heuristic_lcv      | ##################               |    151.304
heuristic_simple   | ####################             |    163.949
csp_ac3            | ################################ |    257.322
```

### Average Nodes

```text
min_conflicts      | #                                |      0.000
dlx                | #                                |    825.429
baseline           | ################################ |  52331.200
heuristic_lcv      | #                                |   1805.000
heuristic_simple   | #                                |   2773.333
csp_ac3            | #                                |    705.667
```

### Slowest Puzzles (by time)

```text
dlx:
  size_16/samimsu_level273 |     66.628 ms | nodes=3803
  size_16/samimsu_level258 |     22.113 ms | nodes=906
  size_16/samimsu_level253 |     10.522 ms | nodes=357
baseline:
  size_16/samimsu_level273 |     45.888 ms | nodes=134056
  size_16/samimsu_level258 |     22.016 ms | nodes=65208
  size_16/samimsu_level310 |     13.201 ms | nodes=38584
heuristic_simple:
  size_16/samimsu_level258 |    178.691 ms | nodes=2608
  size_16/samimsu_level253 |    171.331 ms | nodes=3344
  size_16/samimsu_level310 |    141.825 ms | nodes=2368
heuristic_lcv:
  size_16/samimsu_level253 |    151.304 ms | nodes=1805
csp_ac3:
  size_16/samimsu_level310 |    388.568 ms | nodes=1044
  size_16/samimsu_level253 |    229.965 ms | nodes=725
  size_16/samimsu_level273 |    153.433 ms | nodes=348
```

### Timeouts by Algorithm

```text
baseline           |   2 /   7 |  28.57%
csp_ac3            |   4 /   7 |  57.14%
dlx                |   0 /   7 |   0.00%
heuristic_lcv      |   6 /   7 |  85.71%
heuristic_simple   |   4 /   7 |  57.14%
min_conflicts      |   7 /   7 | 100.00%
```

## Size 17

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| min_conflicts | 2 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| baseline | 2 | 1 | 50.00% | 2.056 | 2.056 | 5508.0 | 315.0 |
| csp_ac3 | 2 | 1 | 50.00% | 15.897 | 15.897 | 21.0 | 4.0 |
| dlx | 2 | 2 | 100.00% | 18.565 | 18.565 | 810.5 | 793.5 |
| heuristic_simple | 2 | 1 | 50.00% | 21.539 | 21.539 | 249.0 | 138.0 |
| heuristic_lcv | 2 | 1 | 50.00% | 27.032 | 27.032 | 184.0 | 106.0 |

### Average Time (ms)

```text
min_conflicts      | #                                |      0.000
baseline           | ##                               |      2.056
csp_ac3            | ##################               |     15.897
dlx                | #####################            |     18.565
heuristic_simple   | #########################        |     21.539
heuristic_lcv      | ################################ |     27.032
```

### Average Nodes

```text
min_conflicts      | #                                |      0.000
baseline           | ################################ |   5508.000
csp_ac3            | #                                |     21.000
dlx                | ####                             |    810.500
heuristic_simple   | #                                |    249.000
heuristic_lcv      | #                                |    184.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_17/samimsu_level213 |      2.056 ms | nodes=5508
heuristic_simple:
  size_17/samimsu_level213 |     21.539 ms | nodes=249
heuristic_lcv:
  size_17/samimsu_level213 |     27.032 ms | nodes=184
dlx:
  size_17/samimsu_level213 |     28.113 ms | nodes=1245
  size_17/samimsu_level302 |      9.017 ms | nodes=376
csp_ac3:
  size_17/samimsu_level213 |     15.897 ms | nodes=21
```

### Timeouts by Algorithm

```text
baseline           |   1 /   2 |  50.00%
csp_ac3            |   1 /   2 |  50.00%
dlx                |   0 /   2 |   0.00%
heuristic_lcv      |   1 /   2 |  50.00%
heuristic_simple   |   1 /   2 |  50.00%
min_conflicts      |   2 /   2 | 100.00%
```

## Size 18

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heuristic_simple | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| heuristic_lcv | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| csp_ac3 | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| min_conflicts | 4 | 0 | 0.00% | 0.000 | 0.000 | 0.0 | 0.0 |
| dlx | 4 | 4 | 100.00% | 24.586 | 5.089 | 985.5 | 967.5 |
| baseline | 4 | 1 | 25.00% | 156.374 | 156.374 | 458433.0 | 25459.0 |

### Average Time (ms)

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
min_conflicts      | #                                |      0.000
dlx                | #####                            |     24.586
baseline           | ################################ |    156.374
```

### Average Nodes

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
csp_ac3            | #                                |      0.000
min_conflicts      | #                                |      0.000
dlx                | #                                |    985.500
baseline           | ################################ | 458433.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_18/samimsu_level229 |    156.374 ms | nodes=458433
dlx:
  size_18/samimsu_level229 |     84.668 ms | nodes=3734
  size_18/samimsu_level373 |      5.325 ms | nodes=91
  size_18/samimsu_level409 |      4.853 ms | nodes=95
```

### Timeouts by Algorithm

```text
baseline           |   3 /   4 |  75.00%
csp_ac3            |   4 /   4 | 100.00%
dlx                |   0 /   4 |   0.00%
heuristic_lcv      |   4 /   4 | 100.00%
heuristic_simple   |   4 /   4 | 100.00%
min_conflicts      |   4 /   4 | 100.00%
```

## Size 6

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 45 | 45 | 100.00% | 0.160 | 0.152 | 307.8 | 47.8 |
| dlx | 45 | 45 | 100.00% | 0.425 | 0.343 | 9.1 | 3.1 |
| heuristic_simple | 45 | 45 | 100.00% | 0.437 | 0.436 | 42.8 | 20.8 |
| csp_ac3 | 45 | 45 | 100.00% | 0.587 | 0.479 | 11.1 | 5.1 |
| heuristic_lcv | 45 | 45 | 100.00% | 0.664 | 0.548 | 37.7 | 17.8 |
| min_conflicts | 45 | 13 | 28.89% | 256.804 | 213.479 | 23854.5 | 4.8 |

### Average Time (ms)

```text
baseline           | #                                |      0.160
dlx                | #                                |      0.425
heuristic_simple   | #                                |      0.437
csp_ac3            | #                                |      0.587
heuristic_lcv      | #                                |      0.664
min_conflicts      | ################################ |    256.804
```

### Average Nodes

```text
baseline           | #                                |    307.800
dlx                | #                                |      9.089
heuristic_simple   | #                                |     42.800
csp_ac3            | #                                |     11.133
heuristic_lcv      | #                                |     37.689
min_conflicts      | ################################ |  23854.462
```

### Slowest Puzzles (by time)

```text
baseline:
  size_6/samimsu_level262 |      0.406 ms | nodes=855
  size_6/samimsu_level337 |      0.398 ms | nodes=843
  size_6/samimsu_level463 |      0.345 ms | nodes=411
heuristic_simple:
  size_6/samimsu_level337 |      1.075 ms | nodes=114
  size_6/samimsu_level139 |      0.927 ms | nodes=95
  size_6/samimsu_level382 |      0.907 ms | nodes=73
heuristic_lcv:
  size_6/samimsu_level337 |      1.911 ms | nodes=121
  size_6/samimsu_level377 |      1.436 ms | nodes=103
  size_6/samimsu_level10 |      1.390 ms | nodes=87
dlx:
  size_6/samimsu_level432 |      0.904 ms | nodes=6
  size_6/samimsu_level337 |      0.893 ms | nodes=18
  size_6/samimsu_level358 |      0.876 ms | nodes=10
csp_ac3:
  size_6/samimsu_level337 |      1.826 ms | nodes=31
  size_6/samimsu_level178 |      1.206 ms | nodes=20
  size_6/samimsu_level109 |      1.183 ms | nodes=25
min_conflicts:
  size_6/samimsu_level304 |    488.625 ms | nodes=45014
  size_6/samimsu_level167 |    485.922 ms | nodes=45007
  size_6/samimsu_level395 |    428.170 ms | nodes=40002
```

### Timeouts by Algorithm

```text
baseline           |   0 /  45 |   0.00%
csp_ac3            |   0 /  45 |   0.00%
dlx                |   0 /  45 |   0.00%
heuristic_lcv      |   0 /  45 |   0.00%
heuristic_simple   |   0 /  45 |   0.00%
min_conflicts      |  32 /  45 |  71.11%
```

## Size 7

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 156 | 156 | 100.00% | 0.403 | 0.237 | 887.7 | 122.8 |
| dlx | 156 | 156 | 100.00% | 0.609 | 0.451 | 12.4 | 5.4 |
| heuristic_simple | 156 | 156 | 100.00% | 1.043 | 0.695 | 86.6 | 44.4 |
| heuristic_lcv | 156 | 156 | 100.00% | 1.298 | 0.945 | 65.8 | 32.4 |
| csp_ac3 | 156 | 156 | 100.00% | 1.366 | 0.864 | 18.6 | 11.6 |
| min_conflicts | 156 | 35 | 22.44% | 190.475 | 206.887 | 13594.0 | 2.7 |

### Average Time (ms)

```text
baseline           | #                                |      0.403
dlx                | #                                |      0.609
heuristic_simple   | #                                |      1.043
heuristic_lcv      | #                                |      1.298
csp_ac3            | #                                |      1.366
min_conflicts      | ################################ |    190.475
```

### Average Nodes

```text
baseline           | ##                               |    887.744
dlx                | #                                |     12.423
heuristic_simple   | #                                |     86.583
heuristic_lcv      | #                                |     65.763
csp_ac3            | #                                |     18.609
min_conflicts      | ################################ |  13593.971
```

### Slowest Puzzles (by time)

```text
baseline:
  size_7/samimsu_level177 |      1.932 ms | nodes=3528
  size_7/samimsu_level211 |      1.833 ms | nodes=4235
  size_7/samimsu_level8 |      1.723 ms | nodes=3871
heuristic_simple:
  size_7/samimsu_level177 |      4.760 ms | nodes=446
  size_7/samimsu_level42 |      3.908 ms | nodes=350
  size_7/samimsu_level394 |      3.787 ms | nodes=320
heuristic_lcv:
  size_7/samimsu_level31 |      5.764 ms | nodes=326
  size_7/samimsu_level315 |      4.827 ms | nodes=272
  size_7/samimsu_level135 |      4.379 ms | nodes=265
dlx:
  size_7/samimsu_level448 |      4.032 ms | nodes=10
  size_7/samimsu_level73 |      2.364 ms | nodes=12
  size_7/samimsu_level91 |      1.580 ms | nodes=11
csp_ac3:
  size_7/samimsu_level148 |      6.619 ms | nodes=110
  size_7/samimsu_level331 |      6.066 ms | nodes=92
  size_7/samimsu_level443 |      5.672 ms | nodes=86
min_conflicts:
  size_7/samimsu_level53 |    486.699 ms | nodes=35003
  size_7/samimsu_level54 |    423.717 ms | nodes=30247
  size_7/samimsu_level98 |    422.664 ms | nodes=30005
```

### Timeouts by Algorithm

```text
baseline           |   0 / 156 |   0.00%
csp_ac3            |   0 / 156 |   0.00%
dlx                |   0 / 156 |   0.00%
heuristic_lcv      |   0 / 156 |   0.00%
heuristic_simple   |   0 / 156 |   0.00%
min_conflicts      | 121 / 156 |  77.56%
```

## Size 8

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 54 | 54 | 100.00% | 0.800 | 0.724 | 14.2 | 6.2 |
| baseline | 54 | 54 | 100.00% | 2.167 | 0.998 | 5173.0 | 642.1 |
| heuristic_simple | 54 | 54 | 100.00% | 5.224 | 3.021 | 386.8 | 218.5 |
| heuristic_lcv | 54 | 54 | 100.00% | 5.363 | 2.448 | 258.9 | 141.9 |
| csp_ac3 | 54 | 54 | 100.00% | 6.220 | 2.128 | 77.1 | 69.1 |
| min_conflicts | 54 | 5 | 9.26% | 265.413 | 353.669 | 15018.0 | 3.0 |

### Average Time (ms)

```text
dlx                | #                                |      0.800
baseline           | #                                |      2.167
heuristic_simple   | #                                |      5.224
heuristic_lcv      | #                                |      5.363
csp_ac3            | #                                |      6.220
min_conflicts      | ################################ |    265.413
```

### Average Nodes

```text
dlx                | #                                |     14.222
baseline           | ###########                      |   5173.037
heuristic_simple   | #                                |    386.778
heuristic_lcv      | #                                |    258.889
csp_ac3            | #                                |     77.056
min_conflicts      | ################################ |  15018.000
```

### Slowest Puzzles (by time)

```text
baseline:
  size_8/samimsu_level274 |      9.261 ms | nodes=21756
  size_8/samimsu_level365 |      8.187 ms | nodes=19796
  size_8/samimsu_level22 |      6.206 ms | nodes=15292
heuristic_simple:
  size_8/samimsu_level274 |     21.079 ms | nodes=1643
  size_8/samimsu_level300 |     18.806 ms | nodes=1448
  size_8/samimsu_level430 |     18.339 ms | nodes=1425
heuristic_lcv:
  size_8/samimsu_level22 |     39.704 ms | nodes=2311
  size_8/samimsu_level274 |     34.301 ms | nodes=1770
  size_8/samimsu_level441 |     32.431 ms | nodes=1805
dlx:
  size_8/samimsu_level360 |      1.562 ms | nodes=25
  size_8/samimsu_level251 |      1.476 ms | nodes=29
  size_8/samimsu_level22 |      1.461 ms | nodes=19
csp_ac3:
  size_8/samimsu_level22 |     55.336 ms | nodes=829
  size_8/samimsu_level441 |     51.644 ms | nodes=717
  size_8/samimsu_level189 |     23.318 ms | nodes=340
min_conflicts:
  size_8/samimsu_level346 |    445.602 ms | nodes=25046
  size_8/samimsu_level24 |    438.849 ms | nodes=25003
  size_8/samimsu_level349 |    353.669 ms | nodes=20012
```

### Timeouts by Algorithm

```text
baseline           |   0 /  54 |   0.00%
csp_ac3            |   0 /  54 |   0.00%
dlx                |   0 /  54 |   0.00%
heuristic_lcv      |   0 /  54 |   0.00%
heuristic_simple   |   0 /  54 |   0.00%
min_conflicts      |  49 /  54 |  90.74%
```

## Size 9

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 49 | 49 | 100.00% | 1.177 | 1.140 | 25.4 | 16.4 |
| baseline | 49 | 49 | 100.00% | 5.989 | 3.681 | 14920.2 | 1652.8 |
| heuristic_simple | 49 | 49 | 100.00% | 16.492 | 11.017 | 1009.6 | 581.4 |
| heuristic_lcv | 49 | 49 | 100.00% | 16.934 | 4.782 | 685.8 | 389.4 |
| csp_ac3 | 49 | 49 | 100.00% | 24.102 | 6.697 | 241.4 | 232.4 |
| min_conflicts | 49 | 3 | 6.12% | 147.051 | 109.818 | 6695.7 | 1.3 |

### Average Time (ms)

```text
dlx                | #                                |      1.177
baseline           | #                                |      5.989
heuristic_simple   | ###                              |     16.492
heuristic_lcv      | ###                              |     16.934
csp_ac3            | #####                            |     24.102
min_conflicts      | ################################ |    147.051
```

### Average Nodes

```text
dlx                | #                                |     25.429
baseline           | ################################ |  14920.163
heuristic_simple   | ##                               |   1009.551
heuristic_lcv      | #                                |    685.755
csp_ac3            | #                                |    241.388
min_conflicts      | ##############                   |   6695.667
```

### Slowest Puzzles (by time)

```text
baseline:
  size_9/samimsu_level280 |     28.653 ms | nodes=71199
  size_9/samimsu_level352 |     24.353 ms | nodes=60201
  size_9/samimsu_level55 |     18.493 ms | nodes=46278
heuristic_simple:
  size_9/samimsu_level55 |     70.879 ms | nodes=4756
  size_9/samimsu_level208 |     64.421 ms | nodes=4022
  size_9/samimsu_level352 |     60.973 ms | nodes=4038
heuristic_lcv:
  size_9/samimsu_level352 |     85.350 ms | nodes=3833
  size_9/samimsu_level428 |     79.353 ms | nodes=3340
  size_9/samimsu_level94 |     57.275 ms | nodes=2302
dlx:
  size_9/samimsu_level437 |      2.430 ms | nodes=111
  size_9/samimsu_level352 |      2.372 ms | nodes=133
  size_9/samimsu_level318 |      2.277 ms | nodes=92
csp_ac3:
  size_9/samimsu_level428 |    131.300 ms | nodes=1489
  size_9/samimsu_level352 |    125.985 ms | nodes=1403
  size_9/samimsu_level321 |     86.392 ms | nodes=858
min_conflicts:
  size_9/samimsu_level461 |    221.720 ms | nodes=10044
  size_9/samimsu_level141 |    109.818 ms | nodes=5033
  size_9/samimsu_level48 |    109.614 ms | nodes=5010
```

### Timeouts by Algorithm

```text
baseline           |   0 /  49 |   0.00%
csp_ac3            |   0 /  49 |   0.00%
dlx                |   0 /  49 |   0.00%
heuristic_lcv      |   0 /  49 |   0.00%
heuristic_simple   |   0 /  49 |   0.00%
min_conflicts      |  46 /  49 |  93.88%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.