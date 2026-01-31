# Queens Solvers Overview

This document explains the solving strategies available in this project and
when each is useful.

## Available Solvers

### dlx
- **Approach**: Exact cover formulation solved with Algorithm X + Dancing Links.
- **Why it’s fast**: chooses the tightest constraint first and uses O(1) cover/uncover.
- **Best for**: general solving, uniqueness checks, and benchmarking baselines.

### baseline
- **Approach**: plain row-by-row backtracking with constraint checks.
- **Strengths**: simple, easy to understand, reliable for small/medium puzzles.
- **Weaknesses**: explores a huge search space; high node/backtrack counts.

### backtracking_bb
- **Approach**: backtracking with MRV row choice + branch-and-bound pruning + LCV
  ordering (local least-constraining value).
- **Pruning**: rejects branches where remaining rows/cols/regions can’t possibly be
  satisfied; also checks for columns/regions with zero available placements.
- **Strengths**: much faster than baseline on harder puzzles while still simple.
- **Weaknesses**: still exponential; not as fast as DLX for large n.

### heuristic_simple
- **Approach**: heuristic-driven backtracking with a lightweight variable-ordering.
- **Strengths**: faster than baseline on many puzzles.
- **Weaknesses**: may still hit timeouts on hard instances.

### heuristic_lcv
- **Approach**: heuristic backtracking with MRV + LCV ordering.
- **Strengths**: better pruning than heuristic_simple, good general performance.
- **Weaknesses**: still slower than DLX and can time out on difficult puzzles.

### csp_ac3
- **Approach**: constraint propagation (AC-3) + backtracking.
- **Strengths**: reduces domains early; good educational CSP reference.
- **Weaknesses**: propagation overhead can outweigh gains on easy puzzles.

## Notes
- All solvers enforce: one queen per row/col/region, no adjacency, and connected regions.
- `dlx` is the reference solver for performance; others are pedagogical baselines.
