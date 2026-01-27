# CSP + AC-3 for Queens

This document explains the CSP + AC-3 solver used for the LinkedIn Queens puzzle.

## 1) Variables and domains
We use one variable per row:
- Variable: `R_r` for each row `r`
- Domain: set of columns `0..n-1`

A value assignment `R_r = c` means a queen is placed at `(r, c)`.

## 2) Constraints
We enforce:
- **Columns**: all rows choose distinct columns
- **Regions**: all rows choose distinct regions
- **Adjacency**: no two queens are adjacent (8-neighborhood)
- **Blocked cells**: forbidden `(r, c)` are removed from domains
- **Givens**: given queen forces the domain to a single value

## 3) AC-3 (Arc Consistency)
AC-3 repeatedly removes values that are inconsistent with neighbors:
- For each pair of rows `(r1, r2)`, remove a column `c1` from `R_r1`
  if there is **no** value `c2` in `R_r2` that can coexist with `(r1, c1)`.

This prunes domains before and during search, often drastically.

## 4) Search + heuristics
After AC-3, we do backtracking with:
- **MRV** (Minimum Remaining Values) to choose the next row
- **LCV** (Least Constraining Value) for value ordering

## 5) Metrics
We track:
- `nodes` = number of assignments tried
- `backtracks` = number of dead-ends
- `time_ms` = elapsed wall-clock time

## 6) Solver location
Implementation: `src/linkedin_game_solver/games/queens/solver_csp.py`
