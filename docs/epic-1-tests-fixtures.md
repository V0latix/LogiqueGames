# Epic 1 — Stabilisation des tests (fixtures manquantes)
> Statut : In Progress
> Priorité : Haute

## Contexte
23 tests sur 59 échouent à cause de fixtures manquantes dans `data/curated/queens/` et `data/curated/zip/`. Ces fixtures (`example_6x6.json`, `zip_n4_01.json`, etc.) sont référencées dans les tests mais les fichiers n'existent pas dans le dépôt.

## Objectif
Tous les tests passent (0 failing). Coverage > 80% sur les solvers.

## Stories
- [Story 1.1](stories/story-1.1-queens-fixtures.md) : Créer les fixtures de test Queens manquantes
- [Story 1.2](stories/story-1.2-zip-fixtures.md) : Créer les fixtures de test Zip manquantes
- [Story 1.3](stories/story-1.3-coverage.md) : Vérifier et compléter la couverture des solvers
