# Todo — LinkedIn Games Solver

## ✅ Corrigé

- [x] **06_grids_to_zip_puzzles.py** — détection des murs implémentée (`detect_walls` via analyse d'épaisseur de ligne)

- [x] **smoke_test_pipeline.py** — scripts 06 et 07 absents du smoke test + ajout flag `--game zip|queens`
- [x] **Pipeline Queens** — `06_grids_to_queens_puzzles.py` + `07_export_site_queens_format.py` créés (playlist : PLLE2dY85AtncQz6UthvQyuFPt812jh3b6)
- [x] **05_export_archive.py** — interpolation puzzle_number incorrecte (`max(prev, next)` → midpoint)

## 🔴 Critique

- [ ] **Réparer les fixtures de tests manquantes**
  `data/curated/queens/` et `data/curated/zip/` sont vides → 23 tests sur 59 échouent (`FileNotFoundError`).
  Créer `example_6x6.json` et `zip_n4_01.json` via le générateur ou les versionner en JSON.

## 🟡 Court terme

- [ ] **Augmenter le dataset web (3 → 50+ puzzles)**
  Lancer le pipeline `scripts/01→07` sur une playlist YouTube et mettre à jour
  `web/public/data/queens_unique.json` et `zip_unique.json`.

- [ ] **Ajouter un bouton "Solve" dans le frontend**
  Afficher la solution d'un puzzle Queens ou Zip en appelant les solvers embarqués dans `App.tsx`.

- [ ] **Configurer GitHub Actions CI**
  Ajouter `.github/workflows/ci.yml` qui lance `pytest` + `tsc` à chaque push.


## 🟢 Moyen terme

- [ ] **Ajouter la sélection de puzzle par ID**
  Permettre à l'utilisateur de choisir un puzzle spécifique (pas seulement le premier).

- [ ] **Découper App.tsx en composants**
  Séparer le monolithe (1249 lignes) en composants : `QueensGame`, `ZipGame`, `StatsBar`, etc.
