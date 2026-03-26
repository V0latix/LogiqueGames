# Story 2.1 — Bouton "Solve" — afficher la solution
> Epic : Epic 2 — Features Frontend
> Statut : Backlog
> Priorité : Moyenne

## Description
En tant que joueur, je veux cliquer un bouton "Solve" pour voir la solution du puzzle courant affichée sur la grille.

## Acceptance Criteria
- [ ] Bouton "Solve" visible dans l'UI Queens et Zip
- [ ] Cliquer affiche la solution sur la grille (reines positionnées / chemin Zip)
- [ ] État `showSolution: boolean` distinct de l'état de jeu
- [ ] Bouton "Hide Solution" pour masquer
- [ ] Pas de refactoring de App.tsx requis — ajouter uniquement un state + rendu conditionnel

## Notes techniques
- Solver inline déjà présent dans `App.tsx` — appeler la fonction existante
- Queens : colorier les cases avec les reines de la solution
- Zip : afficher le chemin numéroté en overlay
- Gérer le cas solver failure (afficher message d'erreur)
