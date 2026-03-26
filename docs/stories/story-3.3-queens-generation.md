# Story 3.3 — Génération procédurale Queens (20+ par taille)
> Epic : Epic 3 — Croissance du dataset
> Statut : Backlog
> Priorité : Basse

## Description
Générer automatiquement 20+ puzzles Queens valides à solution unique pour chaque taille (6x6, 7x7, 8x8) en utilisant le générateur existant.

## Acceptance Criteria
- [ ] 20+ puzzles 6x6 dans `data/curated/queens/`
- [ ] 20+ puzzles 7x7 dans `data/curated/queens/`
- [ ] 20+ puzzles 8x8 dans `data/curated/queens/`
- [ ] Chaque puzzle a une solution unique (vérifié par solver)
- [ ] `web/public/data/queens_unique.json` mis à jour

## Notes techniques
- Le générateur existe déjà : `linkedin_game_solver.games.queens.generator`
- Vérifier l'unicité avec le solver DLX (le plus rapide)
- Script batch à créer ou via CLI `lgs`
