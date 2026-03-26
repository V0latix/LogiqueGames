# PRD — LinkedIn Games Solver
> Généré le 2026-03-26 via /workflows/bmad-brownfield

## Contexte & Problème

LinkedIn propose deux mini-jeux quotidiens (Queens et Zip) sans interface d'entraînement ni datasets ouverts. Ce projet répond à deux besoins :
1. **Exploration algorithmique** : comparer des approches de résolution (DLX, CSP, heuristiques…)
2. **Accès aux puzzles** : jouer à des puzzles hors de LinkedIn, dans le navigateur

**Contrainte** : pas de scraping LinkedIn. Source = vidéos YouTube + génération procédurale.

## Utilisateurs

- **Romain (dev/chercheur)** : utilise le CLI Python pour générer, benchmarker et analyser les algorithmes
- **Joueur casual** : accède au site web pour jouer aux puzzles Queens/Zip

## Périmètre actuel (livré)

### Backend Python
- [x] Solver Queens : 7 algorithmes (baseline, DLX, CSP, heuristiques, B&B)
- [x] Solver Zip : 5 algorithmes
- [x] Générateur Queens (flood-fill + validation unicité)
- [x] Générateur Zip
- [x] CLI `lgs` avec toutes les commandes
- [x] Pipeline d'extraction vidéo (scripts 00→07)
- [x] Import dataset externe (samimsu)
- [x] Benchmarks JSONL + rapport

### Frontend Web
- [x] SPA React — jouable Queens et Zip
- [x] 3 puzzles par jeu (dataset minimal)
- [x] Stats localStorage (completed, streak)
- [x] Design dark, mobile responsive

## Périmètre planifié (backlog)

### Dataset
- [ ] Augmenter le nombre de puzzles (pipeline → 50+ puzzles)
- [ ] Puzzles par taille/difficulté

### Frontend
- [ ] Affichage de la solution (bouton "Solve")
- [ ] Sélection du puzzle par ID
- [ ] Historique des puzzles résolus

### Backend
- [x] Tests unitaires : 27 fichiers, 36 passing
- [x] Corriger les 23 tests en échec (fixtures créées dans `data/curated/`) — 59/59 ✅
- [ ] Solver Zip : nouveaux algorithmes
- [ ] Support d'autres jeux LinkedIn (Tango, Crossclimb)

## Métriques de succès
- Couverture de tests > 80% sur les solvers
- Pipeline reproductible : extraction de 50+ puzzles Zip valides
- Site : 3+ puzzles jouables par jeu avec solution visualisable
