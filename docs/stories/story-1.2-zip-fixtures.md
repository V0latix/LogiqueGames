# Story 1.2 — Créer les fixtures de test Zip manquantes
> Epic : Epic 1 — Stabilisation des tests
> Statut : Done
> Priorité : Haute

## Description
Les tests dans `tests/test_zip_*.py` référencent `data/curated/zip/zip_n4_01.json` qui n'existe pas dans le dépôt.

## Acceptance Criteria
- [x] `data/curated/zip/zip_n4_01.json` créé avec un puzzle Zip 4x4 valide
- [x] 11 tests Zip passent (parser, validator, renderer, solvers, new_solvers, bench)
- [x] Le fichier respecte le format spec (champs `game`, `n`, `numbers`, `walls`)
- [x] Solvable par tous les solvers Zip (baseline, heuristic, forced, articulation)

## Notes techniques
- Format attendu :
  ```json
  { "game": "zip", "id": "zip_n4_01", "n": 4, "numbers": [{"k":1,"r":0,"c":0}, ...], "walls": [{"r1":0,"c1":0,"r2":0,"c2":1}, ...] }
  ```
- Créer un puzzle 4x4 minimal avec solution connue (chemin hamiltonien simple)
- Valider avec `solve_baseline` en premier

## Commandes de vérification
```bash
source .venv/bin/activate
python -m pytest tests/test_zip_solvers.py tests/test_zip_parser.py tests/test_zip_validator.py tests/test_zip_renderer.py -v
```
