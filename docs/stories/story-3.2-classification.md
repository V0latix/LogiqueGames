# Story 3.2 — Classification par taille et difficulté
> Epic : Epic 3 — Croissance du dataset
> Statut : Backlog
> Priorité : Basse

## Description
Ajouter des métadonnées de classification (taille n, difficulté) aux puzzles pour permettre le filtrage dans le frontend.

## Acceptance Criteria
- [ ] Chaque puzzle JSON a un champ `metadata.size` (n=4,5,6,7+)
- [ ] Champ `metadata.difficulty` (easy/medium/hard) basé sur le % de cellules pré-remplies
- [ ] Le frontend peut filtrer par taille et difficulté
