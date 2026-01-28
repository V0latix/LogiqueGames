# linkedin-game-solver

Educational puzzle solver framework in Python. The first implemented game is LinkedIn **Queens**.

## Quickstart

```bash
python -m pytest
ruff check .
```

## CLI

The CLI entrypoint is `lgs`.

Generate and solve a puzzle:

```bash
lgs generate-solve --n 6 --seed 123 --render
```

Generate a dataset (multiple sizes):

```bash
lgs generate-dataset --sizes 6,7,8 --count 20 --seed 100 --algo heuristic_lcv
```

Benchmark a dataset (recursive by size):

```bash
lgs bench \
  --game queens \
  --dataset data/generated/queens \
  --algo baseline,heuristic_simple,heuristic_lcv,dlx,csp_ac3,min_conflicts \
  --report reports/queens_bench_all.md \
  --recursive \
  --top-k 3
```

## Algorithms (Pedagogical Overview)

### Baseline Backtracking
**Idea:** place one queen per row. Try each column, and backtrack when constraints are violated.
This is the most direct, readable solver and a strong baseline for comparison.

**Why it works:** it explores the search tree systematically and guarantees a solution if one exists.

**Cost:** exponential in the worst case, but pruning reduces the search space.

**Mini diagram (search tree):**
```
row 0: c0  c1  c2  c3
         |   |
row 1:  c2  dead
```

**Pseudo-code:**
```
solve(row):
  if row == n: return success
  for col in columns:
    if can_place(row, col):
      place(row, col)
      if solve(row+1): return success
      remove(row, col)
  return failure
```

### Heuristic Backtracking (MRV)
**Idea:** instead of “next row in order”, pick the row with the **fewest legal moves** (MRV).
This cuts branching early and usually reduces the search tree.

**Why it helps:** hard choices first shrink the remaining options.

**Mini diagram:**
```
Rows: [0,1,2,3]
Domains sizes: [4,1,3,2]
Pick row 1 (MRV)
```

**Pseudo-code:**
```
row = argmin(domain_size[row])
for col in domain[row]:
  ...
```

### Heuristic Backtracking (MRV + LCV + Forward Checking)
**Idea:**
- MRV chooses the most constrained row
- LCV chooses the least constraining column
- Forward checking rejects a choice early if it wipes out a future row

**Why it helps:** fewer dead-ends, faster solving on harder boards.

**Mini diagram:**
```
Try col 2 → future row has 0 options → reject
Try col 4 → future rows still have options → keep
```

**Pseudo-code:**
```
row = MRV()
for col in LCV(row):
  if forward_check(row, col):
    recurse
```

### DLX (Algorithm X with Dancing Links)
**Idea:** model the puzzle as an **exact cover** problem.
Primary constraints are **row/col/region**, and adjacency is encoded as secondary columns.
DLX makes cover/uncover operations extremely fast during backtracking.

**Why it helps:** very fast on structured, constrained puzzles.

**Mini diagram (exact cover):**
```
rows: placement choices
cols: row_0 col_3 region_2 adj_5_7 ...
select rows so each primary column is hit once
```

**Pseudo-code:**
```
search():
  if no primary columns: success
  c = smallest column
  cover(c)
  for r in rows(c):
    cover(row r)
    if search(): return success
    uncover(row r)
  uncover(c)
```

Docs: `docs/dlx.md`

### CSP + AC-3
**Idea:** treat each row as a variable and each column as a domain value.
AC-3 prunes the domains by enforcing arc-consistency before and during search.
MRV + LCV are used for ordering.

**Why it helps:** strong pruning before exploring assignments.

**Mini diagram (AC-3):**
```
R1 domain {0,1,2}
R2 domain {0}
Remove 0 from R1
```

**Pseudo-code:**
```
AC3(queue):
  while queue:
    (Xi, Xj) = queue.pop()
    if revise(Xi, Xj):
      if domain[Xi] empty: fail
      add neighbors back to queue
```

Docs: `docs/csp_ac3.md`

### Min-Conflicts (Local Search)
**Idea:** start with a random assignment, then repeatedly move the **most conflicted row**
to the column that minimizes conflicts. Use random tie-breaking and restarts.

**Why it helps:** very fast on large boards, but **not guaranteed** to find a solution.

**Mini diagram:**
```
Pick row with max conflicts → move to best column → repeat
```

**Pseudo-code:**
```
for restart in range(R):
  assignment = random()
  for step in range(S):
    if no conflicts: success
    row = argmax(conflicts)
    col = argmin(conflicts_after_move)
    move(row, col)
```

Docs: `docs/min_conflicts.md`

## Metrics (used in benchmarks)

- **nodes**: number of candidate placements tried
- **backtracks**: number of times we undo a choice after hitting a dead-end
- **time_ms**: elapsed wall-clock time

## Notes

- This project is educational only. No live automation on LinkedIn.
