# Min-Conflicts for Queens

This document explains the Min-Conflicts local search solver used for the
LinkedIn Queens puzzle.

## 1) Representation
We keep one queen per row:
- `assignment[row] = col`

This makes it easy to move a queen within a row.

## 2) Conflicts
A queen at `(r, c)` conflicts if it shares:
- the same column
- the same region
- an adjacent cell (8-neighborhood)

## 3) Algorithm (Min-Conflicts)
1. Start with a random assignment (one queen per row).
2. While conflicts remain:
   - pick the **most conflicted row** (max conflicts)
   - move its queen to the column with **minimum conflicts**
   - break ties randomly
3. If no solution within `max_steps`, restart and try again.

## 4) Notes
- Very fast on large boards, but not guaranteed.
- We use multiple restarts for robustness.
- We still respect blocked cells and givens.

## 5) Solver location
Implementation: `src/linkedin_game_solver/games/queens/solver_min_conflicts.py`
