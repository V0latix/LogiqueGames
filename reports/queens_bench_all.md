# Queens Benchmark Report (Recursive)

- Generated: 2026-01-28 00:29:09
- Dataset root: `data/generated/queens`
- Algorithms: baseline, csp_ac3, dlx, heuristic_lcv, heuristic_simple, min_conflicts
- Time limit: 0.5s

## Global Summary

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 450 | 450 | 100.00% | 0.823 | 0.789 | 11.6 | 2.9 |
| heuristic_lcv | 450 | 450 | 100.00% | 2.432 | 0.970 | 67.5 | 33.0 |
| baseline | 450 | 450 | 100.00% | 2.561 | 0.098 | 6731.3 | 582.7 |
| csp_ac3 | 450 | 450 | 100.00% | 4.481 | 1.809 | 30.7 | 21.9 |
| heuristic_simple | 450 | 449 | 99.78% | 6.252 | 0.447 | 332.7 | 197.9 |
| min_conflicts | 450 | 361 | 80.22% | 145.761 | 111.287 | 8262.6 | 1.6 |

## Size 10

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 70 | 70 | 100.00% | 0.970 | 0.831 | 14.7 | 4.7 |
| baseline | 70 | 70 | 100.00% | 1.614 | 0.229 | 4189.0 | 413.4 |
| heuristic_lcv | 70 | 70 | 100.00% | 1.910 | 1.517 | 35.3 | 14.6 |
| csp_ac3 | 70 | 70 | 100.00% | 3.314 | 2.727 | 18.0 | 8.0 |
| heuristic_simple | 70 | 70 | 100.00% | 5.623 | 1.062 | 360.7 | 207.6 |
| min_conflicts | 70 | 49 | 70.00% | 121.321 | 124.875 | 4808.7 | 0.9 |

### Average Time (ms)

```text
dlx                | #                                |      0.970
baseline           | #                                |      1.614
heuristic_lcv      | #                                |      1.910
csp_ac3            | #                                |      3.314
heuristic_simple   | #                                |      5.623
min_conflicts      | ################################ |    121.321
```

### Average Nodes

```text
dlx                | #                                |     14.700
baseline           | ###########################      |   4189.000
heuristic_lcv      | #                                |     35.343
csp_ac3            | #                                |     17.957
heuristic_simple   | ##                               |    360.714
min_conflicts      | ################################ |   4808.653
```

### Slowest Puzzles (by time)

```text
baseline:
  size_10/queens_n10_018_seed198 |     54.272 ms | nodes=141795
  size_10/queens_n10_035_seed435 |     11.478 ms | nodes=29065
  size_10/queens_n10_010_seed410 |      5.952 ms | nodes=16275
heuristic_simple:
  size_10/queens_n10_018_seed198 |    194.336 ms | nodes=13931
  size_10/queens_n10_005_seed405 |     22.577 ms | nodes=1407
  size_10/queens_n10_010_seed410 |     21.436 ms | nodes=1291
heuristic_lcv:
  size_10/queens_n10_020_seed420 |      5.980 ms | nodes=185
  size_10/queens_n10_034_seed434 |      5.259 ms | nodes=194
  size_10/queens_n10_044_seed444 |      4.495 ms | nodes=119
dlx:
  size_10/queens_n10_007_seed187 |      2.158 ms | nodes=10
  size_10/queens_n10_012_seed192 |      1.941 ms | nodes=35
  size_10/queens_n10_040_seed440 |      1.871 ms | nodes=119
csp_ac3:
  size_10/queens_n10_034_seed434 |      9.457 ms | nodes=93
  size_10/queens_n10_045_seed445 |      7.316 ms | nodes=61
  size_10/queens_n10_020_seed420 |      6.555 ms | nodes=49
min_conflicts:
  size_10/queens_n10_005_seed185 |    495.860 ms | nodes=20024
  size_10/queens_n10_034_seed434 |    387.643 ms | nodes=15222
  size_10/queens_n10_013_seed193 |    380.420 ms | nodes=15169
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
min_conflicts      |  21 /  70 |  30.00%
```

## Size 11

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 50 | 50 | 100.00% | 1.044 | 1.008 | 16.4 | 5.4 |
| baseline | 50 | 50 | 100.00% | 4.556 | 1.052 | 11951.3 | 1080.5 |
| heuristic_lcv | 50 | 50 | 100.00% | 5.019 | 2.215 | 141.6 | 74.7 |
| csp_ac3 | 50 | 50 | 100.00% | 8.612 | 4.105 | 51.3 | 40.3 |
| heuristic_simple | 50 | 50 | 100.00% | 12.851 | 3.699 | 675.1 | 412.5 |
| min_conflicts | 50 | 40 | 80.00% | 144.699 | 149.265 | 4746.6 | 0.9 |

### Average Time (ms)

```text
dlx                | #                                |      1.044
baseline           | #                                |      4.556
heuristic_lcv      | #                                |      5.019
csp_ac3            | #                                |      8.612
heuristic_simple   | ##                               |     12.851
min_conflicts      | ################################ |    144.699
```

### Average Nodes

```text
dlx                | #                                |     16.440
baseline           | ################################ |  11951.280
heuristic_lcv      | #                                |    141.600
csp_ac3            | #                                |     51.340
heuristic_simple   | #                                |    675.060
min_conflicts      | ############                     |   4746.550
```

### Slowest Puzzles (by time)

```text
baseline:
  size_11/queens_n11_038_seed488 |     77.686 ms | nodes=204820
  size_11/queens_n11_037_seed487 |     55.079 ms | nodes=143781
  size_11/queens_n11_020_seed470 |     19.371 ms | nodes=50963
heuristic_simple:
  size_11/queens_n11_038_seed488 |    312.409 ms | nodes=16517
  size_11/queens_n11_020_seed470 |     77.465 ms | nodes=4407
  size_11/queens_n11_039_seed489 |     55.741 ms | nodes=2988
heuristic_lcv:
  size_11/queens_n11_041_seed491 |    115.851 ms | nodes=4958
  size_11/queens_n11_011_seed461 |      9.239 ms | nodes=328
  size_11/queens_n11_044_seed494 |      8.709 ms | nodes=253
dlx:
  size_11/queens_n11_017_seed467 |      1.851 ms | nodes=79
  size_11/queens_n11_025_seed475 |      1.555 ms | nodes=60
  size_11/queens_n11_026_seed476 |      1.309 ms | nodes=39
csp_ac3:
  size_11/queens_n11_041_seed491 |    171.411 ms | nodes=1427
  size_11/queens_n11_011_seed461 |     17.355 ms | nodes=146
  size_11/queens_n11_017_seed467 |     14.254 ms | nodes=113
min_conflicts:
  size_11/queens_n11_026_seed476 |    459.012 ms | nodes=15010
  size_11/queens_n11_031_seed481 |    458.398 ms | nodes=15082
  size_11/queens_n11_016_seed466 |    457.435 ms | nodes=15015
```

### Timeouts by Algorithm

```text
baseline           |   0 /  50 |   0.00%
csp_ac3            |   0 /  50 |   0.00%
dlx                |   0 /  50 |   0.00%
heuristic_lcv      |   0 /  50 |   0.00%
heuristic_simple   |   0 /  50 |   0.00%
min_conflicts      |  10 /  50 |  20.00%
```

## Size 12

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dlx | 50 | 50 | 100.00% | 1.460 | 1.362 | 16.4 | 4.4 |
| heuristic_lcv | 50 | 50 | 100.00% | 10.411 | 3.131 | 317.5 | 170.8 |
| baseline | 50 | 50 | 100.00% | 15.556 | 1.795 | 41373.8 | 3441.3 |
| csp_ac3 | 50 | 50 | 100.00% | 20.253 | 5.473 | 138.7 | 126.7 |
| heuristic_simple | 50 | 49 | 98.00% | 33.375 | 5.669 | 1665.9 | 1016.3 |
| min_conflicts | 50 | 41 | 82.00% | 132.561 | 180.754 | 3667.8 | 0.7 |

### Average Time (ms)

```text
dlx                | #                                |      1.460
heuristic_lcv      | ##                               |     10.411
baseline           | ###                              |     15.556
csp_ac3            | ####                             |     20.253
heuristic_simple   | ########                         |     33.375
min_conflicts      | ################################ |    132.561
```

### Average Nodes

```text
dlx                | #                                |     16.360
heuristic_lcv      | #                                |    317.460
baseline           | ################################ |  41373.840
csp_ac3            | #                                |    138.740
heuristic_simple   | #                                |   1665.918
min_conflicts      | ##                               |   3667.805
```

### Slowest Puzzles (by time)

```text
baseline:
  size_12/queens_n12_047_seed547 |    253.739 ms | nodes=672570
  size_12/queens_n12_038_seed538 |     95.503 ms | nodes=255882
  size_12/queens_n12_014_seed514 |     70.673 ms | nodes=187314
heuristic_simple:
  size_12/queens_n12_014_seed514 |    245.607 ms | nodes=14886
  size_12/queens_n12_037_seed537 |    202.677 ms | nodes=9566
  size_12/queens_n12_033_seed533 |    184.752 ms | nodes=8326
heuristic_lcv:
  size_12/queens_n12_030_seed530 |    153.450 ms | nodes=6006
  size_12/queens_n12_014_seed514 |    146.138 ms | nodes=6115
  size_12/queens_n12_003_seed503 |     18.668 ms | nodes=614
dlx:
  size_12/queens_n12_047_seed547 |      5.398 ms | nodes=63
  size_12/queens_n12_033_seed533 |      2.222 ms | nodes=12
  size_12/queens_n12_039_seed539 |      1.750 ms | nodes=39
csp_ac3:
  size_12/queens_n12_014_seed514 |    324.270 ms | nodes=2701
  size_12/queens_n12_030_seed530 |    304.394 ms | nodes=2567
  size_12/queens_n12_003_seed503 |     36.378 ms | nodes=263
min_conflicts:
  size_12/queens_n12_048_seed548 |    387.836 ms | nodes=10716
  size_12/queens_n12_018_seed518 |    375.865 ms | nodes=10409
  size_12/queens_n12_035_seed535 |    368.466 ms | nodes=10007
```

### Timeouts by Algorithm

```text
baseline           |   0 /  50 |   0.00%
csp_ac3            |   0 /  50 |   0.00%
dlx                |   0 /  50 |   0.00%
heuristic_lcv      |   0 /  50 |   0.00%
heuristic_simple   |   1 /  50 |   2.00%
min_conflicts      |   9 /  50 |  18.00%
```

## Size 6

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.038 | 0.033 | 53.1 | 5.3 |
| heuristic_simple | 70 | 70 | 100.00% | 0.131 | 0.110 | 11.2 | 2.9 |
| heuristic_lcv | 70 | 70 | 100.00% | 0.283 | 0.242 | 12.0 | 3.2 |
| dlx | 70 | 70 | 100.00% | 0.371 | 0.297 | 6.9 | 0.9 |
| csp_ac3 | 70 | 70 | 100.00% | 0.456 | 0.420 | 7.8 | 1.8 |
| min_conflicts | 70 | 62 | 88.57% | 156.384 | 106.428 | 14684.0 | 2.9 |

### Average Time (ms)

```text
baseline           | #                                |      0.038
heuristic_simple   | #                                |      0.131
heuristic_lcv      | #                                |      0.283
dlx                | #                                |      0.371
csp_ac3            | #                                |      0.456
min_conflicts      | ################################ |    156.384
```

### Average Nodes

```text
baseline           | #                                |     53.057
heuristic_simple   | #                                |     11.214
heuristic_lcv      | #                                |     11.957
dlx                | #                                |      6.943
csp_ac3            | #                                |      7.757
min_conflicts      | ################################ |  14683.968
```

### Slowest Puzzles (by time)

```text
baseline:
  size_6/queens_n6_022_seed222 |      0.109 ms | nodes=207
  size_6/queens_n6_009_seed109 |      0.099 ms | nodes=189
  size_6/queens_n6_005_seed105 |      0.097 ms | nodes=189
heuristic_simple:
  size_6/queens_n6_005_seed105 |      0.340 ms | nodes=34
  size_6/queens_n6_009_seed109 |      0.339 ms | nodes=33
  size_6/queens_n6_022_seed222 |      0.330 ms | nodes=31
heuristic_lcv:
  size_6/queens_n6_033_seed233 |      1.036 ms | nodes=10
  size_6/queens_n6_022_seed222 |      0.766 ms | nodes=51
  size_6/queens_n6_046_seed246 |      0.734 ms | nodes=10
dlx:
  size_6/queens_n6_011_seed211 |      2.607 ms | nodes=7
  size_6/queens_n6_023_seed223 |      1.713 ms | nodes=6
  size_6/queens_n6_039_seed239 |      0.802 ms | nodes=6
csp_ac3:
  size_6/queens_n6_022_seed222 |      1.185 ms | nodes=26
  size_6/queens_n6_007_seed207 |      0.914 ms | nodes=18
  size_6/queens_n6_018_seed118 |      0.735 ms | nodes=15
min_conflicts:
  size_6/queens_n6_003_seed103 |    483.089 ms | nodes=45010
  size_6/queens_n6_035_seed235 |    476.198 ms | nodes=45007
  size_6/queens_n6_045_seed245 |    426.896 ms | nodes=40004
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
min_conflicts      |   8 /  70 |  11.43%
```

## Size 7

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.067 | 0.048 | 111.2 | 11.9 |
| heuristic_simple | 70 | 70 | 100.00% | 0.253 | 0.185 | 18.9 | 6.8 |
| heuristic_lcv | 70 | 70 | 100.00% | 0.469 | 0.414 | 15.9 | 4.8 |
| dlx | 70 | 70 | 100.00% | 0.563 | 0.425 | 8.5 | 1.5 |
| csp_ac3 | 70 | 70 | 100.00% | 0.837 | 0.743 | 9.9 | 2.9 |
| min_conflicts | 70 | 55 | 78.57% | 155.047 | 139.512 | 11102.5 | 2.2 |

### Average Time (ms)

```text
baseline           | #                                |      0.067
heuristic_simple   | #                                |      0.253
heuristic_lcv      | #                                |      0.469
dlx                | #                                |      0.563
csp_ac3            | #                                |      0.837
min_conflicts      | ################################ |    155.047
```

### Average Nodes

```text
baseline           | #                                |    111.200
heuristic_simple   | #                                |     18.943
heuristic_lcv      | #                                |     15.900
dlx                | #                                |      8.500
csp_ac3            | #                                |      9.914
min_conflicts      | ################################ |  11102.545
```

### Slowest Puzzles (by time)

```text
baseline:
  size_7/queens_n7_017_seed137 |      0.386 ms | nodes=847
  size_7/queens_n7_005_seed255 |      0.296 ms | nodes=665
  size_7/queens_n7_014_seed264 |      0.282 ms | nodes=616
heuristic_simple:
  size_7/queens_n7_017_seed137 |      1.269 ms | nodes=124
  size_7/queens_n7_005_seed255 |      0.937 ms | nodes=91
  size_7/queens_n7_014_seed264 |      0.893 ms | nodes=88
heuristic_lcv:
  size_7/queens_n7_026_seed276 |      1.240 ms | nodes=66
  size_7/queens_n7_002_seed122 |      0.899 ms | nodes=38
  size_7/queens_n7_017_seed137 |      0.832 ms | nodes=48
dlx:
  size_7/queens_n7_014_seed264 |      1.051 ms | nodes=10
  size_7/queens_n7_049_seed299 |      1.004 ms | nodes=13
  size_7/queens_n7_007_seed127 |      0.933 ms | nodes=7
csp_ac3:
  size_7/queens_n7_026_seed276 |      2.046 ms | nodes=32
  size_7/queens_n7_014_seed264 |      1.854 ms | nodes=32
  size_7/queens_n7_002_seed122 |      1.459 ms | nodes=22
min_conflicts:
  size_7/queens_n7_012_seed132 |    485.585 ms | nodes=35004
  size_7/queens_n7_034_seed284 |    418.810 ms | nodes=30004
  size_7/queens_n7_008_seed128 |    413.620 ms | nodes=30010
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
min_conflicts      |  15 /  70 |  21.43%
```

## Size 8

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.097 | 0.060 | 182.4 | 18.3 |
| heuristic_simple | 70 | 70 | 100.00% | 0.394 | 0.281 | 24.6 | 9.6 |
| heuristic_lcv | 70 | 70 | 100.00% | 0.698 | 0.636 | 15.4 | 4.0 |
| dlx | 70 | 70 | 100.00% | 0.729 | 0.658 | 9.8 | 1.8 |
| csp_ac3 | 70 | 70 | 100.00% | 1.305 | 1.198 | 10.5 | 2.5 |
| min_conflicts | 70 | 60 | 85.71% | 149.274 | 89.413 | 8433.9 | 1.7 |

### Average Time (ms)

```text
baseline           | #                                |      0.097
heuristic_simple   | #                                |      0.394
heuristic_lcv      | #                                |      0.698
dlx                | #                                |      0.729
csp_ac3            | #                                |      1.305
min_conflicts      | ################################ |    149.274
```

### Average Nodes

```text
baseline           | #                                |    182.400
heuristic_simple   | #                                |     24.614
heuristic_lcv      | #                                |     15.443
dlx                | #                                |      9.814
csp_ac3            | #                                |     10.543
min_conflicts      | ################################ |   8433.883
```

### Slowest Puzzles (by time)

```text
baseline:
  size_8/queens_n8_014_seed314 |      0.450 ms | nodes=1028
  size_8/queens_n8_024_seed324 |      0.321 ms | nodes=396
  size_8/queens_n8_046_seed346 |      0.285 ms | nodes=652
heuristic_simple:
  size_8/queens_n8_014_seed314 |      1.659 ms | nodes=127
  size_8/queens_n8_029_seed329 |      1.056 ms | nodes=73
  size_8/queens_n8_004_seed304 |      0.999 ms | nodes=59
heuristic_lcv:
  size_8/queens_n8_006_seed146 |      1.366 ms | nodes=59
  size_8/queens_n8_045_seed345 |      1.316 ms | nodes=56
  size_8/queens_n8_046_seed346 |      1.089 ms | nodes=43
dlx:
  size_8/queens_n8_044_seed344 |      1.306 ms | nodes=21
  size_8/queens_n8_026_seed326 |      1.170 ms | nodes=28
  size_8/queens_n8_011_seed311 |      1.163 ms | nodes=9
csp_ac3:
  size_8/queens_n8_006_seed146 |      2.714 ms | nodes=37
  size_8/queens_n8_045_seed345 |      2.346 ms | nodes=26
  size_8/queens_n8_046_seed346 |      1.982 ms | nodes=22
min_conflicts:
  size_8/queens_n8_041_seed341 |    450.905 ms | nodes=25048
  size_8/queens_n8_010_seed310 |    443.783 ms | nodes=25005
  size_8/queens_n8_003_seed303 |    443.125 ms | nodes=25007
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
min_conflicts      |  10 /  70 |  14.29%
```

## Size 9

| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 70 | 70 | 100.00% | 0.282 | 0.124 | 647.9 | 67.0 |
| dlx | 70 | 70 | 100.00% | 0.871 | 0.678 | 11.5 | 2.5 |
| heuristic_simple | 70 | 70 | 100.00% | 1.157 | 0.625 | 70.0 | 36.4 |
| heuristic_lcv | 70 | 70 | 100.00% | 1.257 | 1.029 | 27.4 | 10.2 |
| csp_ac3 | 70 | 70 | 100.00% | 2.276 | 1.859 | 15.4 | 6.4 |
| min_conflicts | 70 | 54 | 77.14% | 153.190 | 110.283 | 7034.5 | 1.4 |

### Average Time (ms)

```text
baseline           | #                                |      0.282
dlx                | #                                |      0.871
heuristic_simple   | #                                |      1.157
heuristic_lcv      | #                                |      1.257
csp_ac3            | #                                |      2.276
min_conflicts      | ################################ |    153.190
```

### Average Nodes

```text
baseline           | ##                               |    647.871
dlx                | #                                |     11.486
heuristic_simple   | #                                |     70.043
heuristic_lcv      | #                                |     27.400
csp_ac3            | #                                |     15.429
min_conflicts      | ################################ |   7034.463
```

### Slowest Puzzles (by time)

```text
baseline:
  size_9/queens_n9_019_seed179 |      2.233 ms | nodes=5274
  size_9/queens_n9_007_seed357 |      1.397 ms | nodes=3168
  size_9/queens_n9_020_seed370 |      1.157 ms | nodes=2808
heuristic_simple:
  size_9/queens_n9_019_seed179 |      9.159 ms | nodes=569
  size_9/queens_n9_037_seed387 |      4.932 ms | nodes=311
  size_9/queens_n9_007_seed357 |      4.595 ms | nodes=331
heuristic_lcv:
  size_9/queens_n9_044_seed394 |      8.656 ms | nodes=431
  size_9/queens_n9_038_seed388 |      2.862 ms | nodes=109
  size_9/queens_n9_048_seed398 |      2.526 ms | nodes=106
dlx:
  size_9/queens_n9_014_seed174 |      4.336 ms | nodes=10
  size_9/queens_n9_021_seed371 |      2.582 ms | nodes=9
  size_9/queens_n9_029_seed379 |      2.292 ms | nodes=9
csp_ac3:
  size_9/queens_n9_044_seed394 |     17.262 ms | nodes=222
  size_9/queens_n9_038_seed388 |      4.150 ms | nodes=30
  size_9/queens_n9_048_seed398 |      3.316 ms | nodes=30
min_conflicts:
  size_9/queens_n9_010_seed360 |    437.768 ms | nodes=20028
  size_9/queens_n9_045_seed395 |    436.671 ms | nodes=20009
  size_9/queens_n9_020_seed370 |    434.477 ms | nodes=20004
```

### Timeouts by Algorithm

```text
baseline           |   0 /  70 |   0.00%
csp_ac3            |   0 /  70 |   0.00%
dlx                |   0 /  70 |   0.00%
heuristic_lcv      |   0 /  70 |   0.00%
heuristic_simple   |   0 /  70 |   0.00%
min_conflicts      |  16 /  70 |  22.86%
```

## Notes

- Times are measured inside each solver using `perf_counter()`.
- Averages and medians are computed over solved puzzles only.
- This report is ASCII-only to stay portable in terminals and GitHub Markdown.