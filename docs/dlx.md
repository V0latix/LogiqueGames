# DLX (Algorithm X) for Queens

This document explains how the DLX solver in this repo models and solves the
LinkedIn Queens puzzle.

## 1) Core idea (Exact Cover)
We transform the puzzle into an **exact cover** problem:
- We build a matrix where **rows = possible queen placements**.
- **Columns = constraints** that must be satisfied.
- A solution is a set of rows covering **each primary column exactly once**.

DLX (Dancing Links) is a data structure that allows very fast cover/uncover
operations during backtracking.

## 2) Primary constraints (must be covered exactly once)
For a board of size `n`:
- `row_r` — one queen in each row
- `col_c` — one queen in each column
- `region_k` — one queen in each region

Each candidate cell `(r, c)` covers exactly these three primary columns:
```
row_r, col_c, region_k
```

## 3) Secondary constraints (at most once)
Queens **cannot be adjacent** (8-neighborhood). This is a "at-most-one"
constraint, not an exact one.

We model this by adding **secondary columns**:
- For each adjacent pair of cells `(a, b)`, create a column like
  `adj_idA_idB`.
- Each candidate placement covers all adjacency columns involving that cell.

DLX treats secondary columns as optional: they can be covered **at most once**,
which enforces the adjacency rule.

## 4) Search strategy
Algorithm X (with DLX):
1. Choose the **smallest primary column** (most constrained).
2. Try each row in that column.
3. Cover all columns in that row.
4. Recurse.
5. Uncover on backtrack.

This is extremely efficient for constrained problems.

## 5) What we measure
We track metrics for benchmarking:
- `nodes`: number of candidate rows tried
- `backtracks`: number of dead-ends
- `time_ms`: elapsed time

## 6) Why DLX is good here
- Handles exact-cover constraints naturally (row/col/region)
- Very fast on medium/large boards
- Clean comparison with backtracking/heuristics

## 7) Solver location
Implementation: `src/linkedin_game_solver/games/queens/solver_dlx.py`
