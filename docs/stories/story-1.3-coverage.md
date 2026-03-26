# Story 1.3 — Compléter la couverture des solvers
> Epic : Epic 1 — Stabilisation des tests
> Statut : Backlog (après 1.1 + 1.2)
> Priorité : Haute

## Description
Après correction des fixtures, s'assurer que la couverture de tests dépasse 80% sur les solvers Queens et Zip.

## Acceptance Criteria
- [ ] `pytest --cov` exécuté et rapport généré
- [ ] Coverage > 80% sur `games/queens/solver_*.py`
- [ ] Coverage > 80% sur `games/zip/solver_*.py`
- [ ] Cas limites testés : puzzle sans solution, solutions multiples, timeout

## Commandes de vérification
```bash
source .venv/bin/activate
pip install pytest-cov
python -m pytest --cov=linkedin_game_solver.games --cov-report=term-missing
```
