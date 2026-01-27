# Queens Benchmark Report (Recursive)

- Generated: 2026-01-27 23:44:56
- Dataset root: `data/imported/queens/samimsu_by_size`
- Algorithms: baseline, dlx, heuristic_lcv, heuristic_simple
- Time limit: 0.5s

## Global Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 473 | 473 | 100.00% | 1.770 | 0.797 | 58.8 | 49.9 |
| baseline | 473 | 450 | 95.14% | 24.788 | 0.761 | 67757.6 | 5787.9 |
| heuristic_lcv | 473 | 420 | 88.79% | 26.466 | 1.717 | 827.2 | 454.7 |
| heuristic_simple | 473 | 428 | 90.49% | 31.171 | 1.825 | 1444.3 | 803.4 |

## Size 10

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 38 | 38 | 100.00% | 1.195 | 0.905 | 25.7 | 15.7 |
| baseline | 38 | 38 | 100.00% | 42.531 | 17.800 | 113921.1 | 11386.6 |
| heuristic_simple | 38 | 36 | 94.74% | 52.810 | 26.273 | 2933.9 | 1528.5 |
| heuristic_lcv | 38 | 36 | 94.74% | 62.797 | 10.924 | 2366.2 | 1181.2 |

### Average Time (ms)

```text
dlx                | #                                |      1.195
baseline           | #####################            |     42.531
heuristic_simple   | ##########################       |     52.810
heuristic_lcv      | ################################ |     62.797
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
  size_10/samimsu_level290 |    246.930 ms | nodes=658955
  size_10/samimsu_level164 |    223.064 ms | nodes=613435
  size_10/samimsu_level232 |    185.382 ms | nodes=494225
heuristic_simple:
  size_10/samimsu_level190 |    355.323 ms | nodes=21293
  size_10/samimsu_level224 |    217.328 ms | nodes=14777
  size_10/samimsu_level19 |    186.691 ms | nodes=11115
heuristic_lcv:
  size_10/samimsu_level224 |    414.398 ms | nodes=18060
  size_10/samimsu_level190 |    349.255 ms | nodes=13917
  size_10/samimsu_level191 |    245.732 ms | nodes=9884
dlx:
  size_10/samimsu_level190 |      3.033 ms | nodes=194
  size_10/samimsu_level164 |      2.704 ms | nodes=44
  size_10/samimsu_level201 |      2.497 ms | nodes=38
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
| dlx | 81 | 81 | 100.00% | 1.804 | 1.197 | 51.9 | 40.9 |
| baseline | 81 | 72 | 88.89% | 70.806 | 28.819 | 189832.7 | 17251.5 |
| heuristic_lcv | 81 | 67 | 82.72% | 82.687 | 33.652 | 2453.3 | 1385.4 |
| heuristic_simple | 81 | 69 | 85.19% | 115.962 | 70.461 | 5407.2 | 3056.7 |

### Average Time (ms)

```text
dlx                | #                                |      1.804
baseline           | ###################              |     70.806
heuristic_lcv      | ######################           |     82.687
heuristic_simple   | ################################ |    115.962
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
  size_11/samimsu_level384 |    307.056 ms | nodes=829807
  size_11/samimsu_level40 |    287.121 ms | nodes=749958
  size_11/samimsu_level294 |    280.277 ms | nodes=756525
heuristic_simple:
  size_11/samimsu_level20 |    442.452 ms | nodes=21263
  size_11/samimsu_level76 |    436.071 ms | nodes=23880
  size_11/samimsu_level181 |    433.276 ms | nodes=25894
heuristic_lcv:
  size_11/samimsu_level187 |    480.783 ms | nodes=14863
  size_11/samimsu_level276 |    467.558 ms | nodes=15151
  size_11/samimsu_level317 |    407.016 ms | nodes=10493
dlx:
  size_11/samimsu_level234 |     10.196 ms | nodes=690
  size_11/samimsu_level256 |      5.099 ms | nodes=20
  size_11/samimsu_level295 |      4.811 ms | nodes=44
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
| dlx | 5 | 5 | 100.00% | 1.886 | 2.004 | 40.8 | 28.8 |
| baseline | 5 | 3 | 60.00% | 201.408 | 135.867 | 558354.0 | 46523.0 |
| heuristic_simple | 5 | 1 | 20.00% | 372.020 | 372.020 | 17702.0 | 9417.0 |

### Average Time (ms)

```text
heuristic_lcv      | #                                |      0.000
dlx                | #                                |      1.886
baseline           | #################                |    201.408
heuristic_simple   | ################################ |    372.020
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
  size_12/samimsu_level223 |      2.176 ms | nodes=32
  size_12/samimsu_level204 |      2.018 ms | nodes=64
  size_12/samimsu_level303 |      2.004 ms | nodes=64
baseline:
  size_12/samimsu_level223 |    359.087 ms | nodes=1001034
  size_12/samimsu_level204 |    135.867 ms | nodes=381834
  size_12/samimsu_level202 |    109.269 ms | nodes=292194
heuristic_simple:
  size_12/samimsu_level202 |    372.020 ms | nodes=17702
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
| dlx | 14 | 14 | 100.00% | 2.907 | 2.043 | 84.0 | 71.0 |
| baseline | 14 | 12 | 85.71% | 45.632 | 5.673 | 128328.4 | 9864.4 |
| heuristic_simple | 14 | 8 | 57.14% | 72.151 | 22.217 | 1929.4 | 1112.2 |
| heuristic_lcv | 14 | 7 | 50.00% | 162.239 | 69.341 | 3747.3 | 2277.9 |

### Average Time (ms)

```text
dlx                | #                                |      2.907
baseline           | #########                        |     45.632
heuristic_simple   | ##############                   |     72.151
heuristic_lcv      | ################################ |    162.239
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
  size_13/samimsu_level278 |    175.785 ms | nodes=491244
  size_13/samimsu_level244 |    148.792 ms | nodes=416741
  size_13/samimsu_level237 |    142.695 ms | nodes=406874
heuristic_simple:
  size_13/samimsu_level221 |    378.049 ms | nodes=10056
  size_13/samimsu_level219 |     81.976 ms | nodes=2082
  size_13/samimsu_level305 |     53.932 ms | nodes=1414
heuristic_lcv:
  size_13/samimsu_level248 |    492.996 ms | nodes=12178
  size_13/samimsu_level279 |    346.157 ms | nodes=8227
  size_13/samimsu_level305 |    154.209 ms | nodes=2688
dlx:
  size_13/samimsu_level237 |      8.835 ms | nodes=373
  size_13/samimsu_level195 |      5.699 ms | nodes=284
  size_13/samimsu_level226 |      3.409 ms | nodes=104
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
| dlx | 4 | 4 | 100.00% | 3.567 | 2.651 | 111.2 | 97.2 |
| heuristic_lcv | 4 | 1 | 25.00% | 6.721 | 6.721 | 81.0 | 38.0 |
| baseline | 4 | 1 | 25.00% | 12.883 | 12.883 | 35889.0 | 2556.0 |
| heuristic_simple | 4 | 1 | 25.00% | 76.207 | 76.207 | 1695.0 | 1059.0 |

### Average Time (ms)

```text
dlx                | #                                |      3.567
heuristic_lcv      | ##                               |      6.721
baseline           | #####                            |     12.883
heuristic_simple   | ################################ |     76.207
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
  size_14/samimsu_level212 |      7.078 ms | nodes=335
  size_14/samimsu_level296 |      3.083 ms | nodes=75
  size_14/samimsu_level228 |      2.219 ms | nodes=21
baseline:
  size_14/samimsu_level296 |     12.883 ms | nodes=35889
heuristic_simple:
  size_14/samimsu_level296 |     76.207 ms | nodes=1695
heuristic_lcv:
  size_14/samimsu_level296 |      6.721 ms | nodes=81
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
| dlx | 14 | 14 | 100.00% | 9.008 | 3.139 | 365.0 | 350.0 |
| heuristic_simple | 14 | 4 | 28.57% | 45.824 | 35.070 | 777.5 | 436.2 |
| baseline | 14 | 13 | 92.86% | 197.045 | 159.763 | 565746.9 | 37708.5 |
| heuristic_lcv | 14 | 3 | 21.43% | 228.531 | 210.600 | 3349.3 | 1935.7 |

### Average Time (ms)

```text
dlx                | #                                |      9.008
heuristic_simple   | ######                           |     45.824
baseline           | ###########################      |    197.045
heuristic_lcv      | ################################ |    228.531
```

### Average Nodes

```text
dlx                | #                                |    365.000
heuristic_simple   | #                                |    777.500
baseline           | ################################ | 565746.923
heuristic_lcv      | #                                |   3349.333
```

### Slowest Puzzles (by time)

```text
baseline:
  size_15/samimsu_level263 |    499.271 ms | nodes=1427910
  size_15/samimsu_level215 |    494.442 ms | nodes=1414830
  size_15/samimsu_level214 |    414.529 ms | nodes=1171635
dlx:
  size_15/samimsu_level205 |     65.538 ms | nodes=3110
  size_15/samimsu_level263 |     15.342 ms | nodes=668
  size_15/samimsu_level306 |      9.150 ms | nodes=504
heuristic_simple:
  size_15/samimsu_level230 |    106.725 ms | nodes=1597
  size_15/samimsu_level271 |     42.949 ms | nodes=690
  size_15/samimsu_level297 |     27.190 ms | nodes=676
heuristic_lcv:
  size_15/samimsu_level230 |    419.128 ms | nodes=5365
  size_15/samimsu_level371 |    210.600 ms | nodes=4062
  size_15/samimsu_level271 |     55.864 ms | nodes=621
```

### Timeouts by Algorithm

```text
baseline           |   1 /  14 |   7.14%
dlx                |   0 /  14 |   0.00%
heuristic_lcv      |  11 /  14 |  78.57%
heuristic_simple   |  10 /  14 |  71.43%
```

## Size 16

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 7 | 5 | 71.43% | 17.504 | 12.869 | 52331.2 | 3262.2 |
| dlx | 7 | 7 | 100.00% | 17.974 | 10.801 | 825.4 | 809.4 |
| heuristic_lcv | 7 | 1 | 14.29% | 147.922 | 147.922 | 1805.0 | 1144.0 |
| heuristic_simple | 7 | 4 | 57.14% | 242.546 | 169.304 | 3866.8 | 2131.0 |

### Average Time (ms)

```text
baseline           | ##                               |     17.504
dlx                | ##                               |     17.974
heuristic_lcv      | ###################              |    147.922
heuristic_simple   | ################################ |    242.546
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
  size_16/samimsu_level273 |     67.188 ms | nodes=3803
  size_16/samimsu_level258 |     22.329 ms | nodes=906
  size_16/samimsu_level253 |     11.595 ms | nodes=357
baseline:
  size_16/samimsu_level273 |     44.861 ms | nodes=134056
  size_16/samimsu_level258 |     21.614 ms | nodes=65208
  size_16/samimsu_level310 |     12.869 ms | nodes=38584
heuristic_simple:
  size_16/samimsu_level273 |    493.921 ms | nodes=7147
  size_16/samimsu_level258 |    171.803 ms | nodes=2608
  size_16/samimsu_level253 |    166.804 ms | nodes=3344
heuristic_lcv:
  size_16/samimsu_level253 |    147.922 ms | nodes=1805
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
| baseline | 2 | 1 | 50.00% | 1.886 | 1.886 | 5508.0 | 315.0 |
| dlx | 2 | 2 | 100.00% | 18.076 | 18.076 | 810.5 | 793.5 |
| heuristic_simple | 2 | 1 | 50.00% | 20.832 | 20.832 | 249.0 | 138.0 |
| heuristic_lcv | 2 | 1 | 50.00% | 26.341 | 26.341 | 184.0 | 106.0 |

### Average Time (ms)

```text
baseline           | ##                               |      1.886
dlx                | #####################            |     18.076
heuristic_simple   | #########################        |     20.832
heuristic_lcv      | ################################ |     26.341
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
  size_17/samimsu_level213 |      1.886 ms | nodes=5508
heuristic_simple:
  size_17/samimsu_level213 |     20.832 ms | nodes=249
heuristic_lcv:
  size_17/samimsu_level213 |     26.341 ms | nodes=184
dlx:
  size_17/samimsu_level213 |     27.498 ms | nodes=1245
  size_17/samimsu_level302 |      8.654 ms | nodes=376
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
| dlx | 4 | 4 | 100.00% | 24.755 | 5.230 | 985.5 | 967.5 |
| baseline | 4 | 1 | 25.00% | 155.486 | 155.486 | 458433.0 | 25459.0 |

### Average Time (ms)

```text
heuristic_simple   | #                                |      0.000
heuristic_lcv      | #                                |      0.000
dlx                | #####                            |     24.755
baseline           | ################################ |    155.486
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
  size_18/samimsu_level229 |    155.486 ms | nodes=458433
dlx:
  size_18/samimsu_level229 |     85.429 ms | nodes=3734
  size_18/samimsu_level409 |      5.304 ms | nodes=95
  size_18/samimsu_level373 |      5.157 ms | nodes=91
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
| baseline | 45 | 45 | 100.00% | 0.146 | 0.142 | 307.8 | 47.8 |
| dlx | 45 | 45 | 100.00% | 0.393 | 0.319 | 9.1 | 3.1 |
| heuristic_simple | 45 | 45 | 100.00% | 0.424 | 0.423 | 42.8 | 20.8 |
| heuristic_lcv | 45 | 45 | 100.00% | 0.596 | 0.549 | 37.7 | 17.8 |

### Average Time (ms)

```text
baseline           | #######                          |      0.146
dlx                | #####################            |      0.393
heuristic_simple   | ######################           |      0.424
heuristic_lcv      | ################################ |      0.596
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
  size_6/samimsu_level337 |      0.387 ms | nodes=843
  size_6/samimsu_level21 |      0.324 ms | nodes=699
heuristic_simple:
  size_6/samimsu_level21 |      1.187 ms | nodes=87
  size_6/samimsu_level337 |      1.049 ms | nodes=114
  size_6/samimsu_level139 |      0.916 ms | nodes=95
heuristic_lcv:
  size_6/samimsu_level337 |      1.704 ms | nodes=121
  size_6/samimsu_level377 |      1.401 ms | nodes=103
  size_6/samimsu_level10 |      1.282 ms | nodes=87
dlx:
  size_6/samimsu_level363 |      0.885 ms | nodes=12
  size_6/samimsu_level425 |      0.766 ms | nodes=6
  size_6/samimsu_level299 |      0.745 ms | nodes=17
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
| baseline | 156 | 156 | 100.00% | 0.386 | 0.227 | 887.7 | 122.8 |
| dlx | 156 | 156 | 100.00% | 0.543 | 0.424 | 12.4 | 5.4 |
| heuristic_simple | 156 | 156 | 100.00% | 1.035 | 0.749 | 86.6 | 44.4 |
| heuristic_lcv | 156 | 156 | 100.00% | 1.269 | 0.922 | 65.8 | 32.4 |

### Average Time (ms)

```text
baseline           | #########                        |      0.386
dlx                | #############                    |      0.543
heuristic_simple   | ##########################       |      1.035
heuristic_lcv      | ################################ |      1.269
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
  size_7/samimsu_level8 |      1.661 ms | nodes=3871
  size_7/samimsu_level91 |      1.600 ms | nodes=3640
heuristic_simple:
  size_7/samimsu_level177 |      4.757 ms | nodes=446
  size_7/samimsu_level42 |      3.845 ms | nodes=350
  size_7/samimsu_level394 |      3.692 ms | nodes=320
heuristic_lcv:
  size_7/samimsu_level31 |      5.420 ms | nodes=326
  size_7/samimsu_level315 |      4.886 ms | nodes=272
  size_7/samimsu_level135 |      4.316 ms | nodes=265
dlx:
  size_7/samimsu_level416 |      1.346 ms | nodes=80
  size_7/samimsu_level102 |      1.248 ms | nodes=36
  size_7/samimsu_level129 |      1.247 ms | nodes=39
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
| dlx | 54 | 54 | 100.00% | 0.740 | 0.576 | 14.2 | 6.2 |
| baseline | 54 | 54 | 100.00% | 2.113 | 0.982 | 5173.0 | 642.1 |
| heuristic_simple | 54 | 54 | 100.00% | 5.106 | 2.973 | 386.8 | 218.5 |
| heuristic_lcv | 54 | 54 | 100.00% | 5.222 | 2.235 | 258.9 | 141.9 |

### Average Time (ms)

```text
dlx                | ####                             |      0.740
baseline           | ############                     |      2.113
heuristic_simple   | ###############################  |      5.106
heuristic_lcv      | ################################ |      5.222
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
  size_8/samimsu_level274 |      8.912 ms | nodes=21756
  size_8/samimsu_level365 |      8.063 ms | nodes=19796
  size_8/samimsu_level22 |      6.207 ms | nodes=15292
heuristic_simple:
  size_8/samimsu_level274 |     20.724 ms | nodes=1643
  size_8/samimsu_level300 |     18.554 ms | nodes=1448
  size_8/samimsu_level22 |     17.970 ms | nodes=1598
heuristic_lcv:
  size_8/samimsu_level22 |     39.344 ms | nodes=2311
  size_8/samimsu_level274 |     33.411 ms | nodes=1770
  size_8/samimsu_level441 |     31.445 ms | nodes=1805
dlx:
  size_8/samimsu_level117 |      3.204 ms | nodes=8
  size_8/samimsu_level24 |      1.922 ms | nodes=8
  size_8/samimsu_level441 |      1.427 ms | nodes=60
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
| dlx | 49 | 49 | 100.00% | 1.059 | 0.987 | 25.4 | 16.4 |
| baseline | 49 | 49 | 100.00% | 5.884 | 3.663 | 14920.2 | 1652.8 |
| heuristic_simple | 49 | 49 | 100.00% | 15.974 | 10.579 | 1009.6 | 581.4 |
| heuristic_lcv | 49 | 49 | 100.00% | 16.450 | 4.458 | 685.8 | 389.4 |

### Average Time (ms)

```text
dlx                | ##                               |      1.059
baseline           | ###########                      |      5.884
heuristic_simple   | ###############################  |     15.974
heuristic_lcv      | ################################ |     16.450
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
  size_9/samimsu_level280 |     28.219 ms | nodes=71199
  size_9/samimsu_level352 |     24.039 ms | nodes=60201
  size_9/samimsu_level55 |     18.304 ms | nodes=46278
heuristic_simple:
  size_9/samimsu_level55 |     68.532 ms | nodes=4756
  size_9/samimsu_level208 |     62.738 ms | nodes=4022
  size_9/samimsu_level352 |     59.286 ms | nodes=4038
heuristic_lcv:
  size_9/samimsu_level352 |     83.737 ms | nodes=3833
  size_9/samimsu_level428 |     76.447 ms | nodes=3340
  size_9/samimsu_level94 |     56.224 ms | nodes=2302
dlx:
  size_9/samimsu_level352 |      2.737 ms | nodes=133
  size_9/samimsu_level437 |      2.491 ms | nodes=111
  size_9/samimsu_level423 |      1.785 ms | nodes=35
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