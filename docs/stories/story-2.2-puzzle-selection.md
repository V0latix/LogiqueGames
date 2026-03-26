# Story 2.2 — Sélection du puzzle par ID
> Epic : Epic 2 — Features Frontend
> Statut : Backlog
> Priorité : Moyenne

## Description
En tant que joueur, je veux naviguer entre les puzzles disponibles (pas seulement le premier chargé).

## Acceptance Criteria
- [ ] Dropdown ou boutons prev/next pour changer de puzzle
- [ ] Le changement de puzzle réinitialise la grille
- [ ] L'ID du puzzle courant est visible
- [ ] Fonctionne pour Queens et Zip

## Notes techniques
- Données déjà chargées depuis `queens_unique.json` / `zip_unique.json`
- Ajouter state `currentPuzzleIndex: number` dans App.tsx
- Pas de router nécessaire — SPA sans URL params pour l'instant
