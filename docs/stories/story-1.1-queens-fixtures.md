# Story 1.1 — Créer les fixtures de test Queens manquantes
> Epic : Epic 1 — Stabilisation des tests
> Statut : Done
> Priorité : Haute

## Description
Les tests dans `tests/test_queens_solvers.py`, `test_queens_parser.py`, `test_queens_validator.py` référencent `data/curated/queens/example_6x6.json` qui n'existe pas dans le dépôt.

## Acceptance Criteria
- [x] `data/curated/queens/example_6x6.json` créé avec un puzzle Queens 6x6 valide
- [x] 12 tests Queens passent (test_queens_solvers, test_queens_parser, test_queens_validator)
- [x] Le fichier respecte le format `spec.md` (champs `game`, `n`, `regions`, `givens`)
- [x] min_conflicts résout le puzzle (seed=42, 2000 steps, 5 restarts)

## Notes techniques
- Utiliser le générateur existant : `from linkedin_game_solver.games.queens.generator import generate_puzzle`
- Format attendu :
  ```json
  { "game": "queens", "id": "example_6x6", "n": 6, "regions": [[...]], "givens": { "queens": [], "blocked": [] } }
  ```
- Vérifier l'unicité avec `solve_dlx` ou `solve_csp_ac3`

## Commandes de vérification
```bash
source .venv/bin/activate
python -m pytest tests/test_queens_solvers.py tests/test_queens_parser.py tests/test_queens_validator.py -v
```
