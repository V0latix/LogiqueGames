# Story 2.3 — Historique des puzzles résolus
> Epic : Epic 2 — Features Frontend
> Statut : Backlog
> Priorité : Basse

## Description
En tant que joueur, je veux voir les puzzles que j'ai déjà résolus avec le temps mis.

## Acceptance Criteria
- [ ] Section "Historique" affiche les N derniers puzzles résolus
- [ ] Chaque entrée : ID puzzle + temps + date
- [ ] Persiste dans localStorage (clé existante `linkedin-games-stats`)
- [ ] Bouton "Effacer" l'historique

## Notes techniques
- Étendre le format localStorage existant (ne pas casser la structure actuelle)
- Limiter à 20 entrées max
