# Project Context — LinkedIn Games Solver
> Généré le 2026-03-26 via /workflows/bmad-brownfield
> **Ce fichier est la constitution du projet. Le lire en premier avant tout développement.**

## Vue d'ensemble

Framework éducatif de résolution de puzzles LinkedIn (Queens et Zip). Deux composantes distinctes :
1. **Python backend** : moteur de solvers, générateurs, benchmarks, pipeline d'extraction vidéo
2. **Web frontend** : SPA React permettant de jouer/visualiser les puzzles directement dans le navigateur

## Technology Stack & Versions

### Backend Python
- Runtime : Python 3.11+
- Package : `linkedin-game-solver` (installable via `pip install -e .`)
- CLI : commande `lgs` (entrypoint `linkedin_game_solver.cli:main`)
- Dépendances clés : numpy, opencv-python, pandas, matplotlib, Pillow
- Tests : pytest (`testpaths = ["tests"]`)
- Lint : ruff (line-length 100)

### Frontend Web
- Runtime : Node.js (LTS)
- Framework : React 18 + TypeScript 5.5
- Bundler : Vite 5.4
- Style : CSS vanilla (index.css ~533 lignes, dark theme)
- Données : JSON statiques dans `web/public/data/`
- Pas de backend API, pas de router — SPA pure monofichier (`App.tsx` ~1249 lignes)

### Pipeline extraction vidéo
- Outils : yt-dlp, ffmpeg
- Scripts numérotés `scripts/00_` → `scripts/07_`

## Structure du projet

```
.
├── src/linkedin_game_solver/
│   ├── core/               # types.py, metrics.py — types et métriques partagés
│   ├── games/
│   │   ├── queens/         # solver_*, generator, parser, renderer, validator
│   │   └── zip/            # solver_*, generator, model, parser, renderer, validator
│   ├── datasets/           # exporter, normalize, organize, unique
│   ├── benchmarks/         # queens.py, zip.py, report_utils.py
│   └── cli.py              # Point d'entrée CLI `lgs`
├── tests/                  # pytest (0 tests actuellement)
├── scripts/                # Pipeline extraction 00→07
├── web/
│   ├── src/
│   │   ├── App.tsx         # Toute la logique frontend (1249 lignes)
│   │   ├── main.tsx        # Entrypoint React
│   │   └── index.css       # Styles globaux dark theme
│   └── public/data/
│       ├── queens_unique.json  # 3 puzzles Queens
│       └── zip_unique.json     # 3 puzzles Zip
├── zip_archive/            # Artefacts pipeline (ignorés par git sauf .gitkeep)
├── spec.md                 # Format de données Queens (source de vérité)
└── docs/                   # Documentation BMAD
```

## Critical Implementation Rules

### Python — Patterns obligatoires
- Structure : chaque jeu dans `src/linkedin_game_solver/games/<game>/`
- Chaque jeu expose : `solver_*.py`, `generator.py`, `parser.py`, `renderer.py`, `validator.py`
- Types partagés dans `core/types.py` — utiliser ces types, ne pas redéfinir
- Format puzzle JSON conforme à `spec.md` (champ `game`, `n`, `regions`, `givens`, `solution`)
- Solvers multiples par jeu : baseline, heuristic, dlx, csp, backtracking_bb, min_conflicts (Queens)
- Benchmarks : output JSONL une ligne par run (cf. spec.md §2.3)

### Frontend — Patterns obligatoires
- **Tout le code est dans `App.tsx`** — pas de découpage en composants séparés pour l'instant
- Types définis en tête de fichier (QueensPuzzle, ZipPuzzle, etc.)
- Types normalisés suffixés `Normalized` (ajout de Sets/Maps pour lookups O(1))
- Stats stockées dans `localStorage` (clé `linkedin-games-stats`)
- Dates au format `YYYY-MM-DD` (fonction `formatDateKey`)
- Pas de dépendances UI tierces (pas de shadcn, pas de Tailwind)

### TypeScript
- `strict: true` dans tsconfig
- Imports relatifs (pas d'alias `@/`)
- Pas de `any` — utiliser les types définis

### Données
- Les puzzles sont des JSON statiques dans `web/public/data/`
- Format Queens : `{ id, n, regions, givens: { queens, blocked } }`
- Format Zip : `{ id, n, numbers: [{k,r,c}], walls: [{r1,c1,r2,c2}] }`
- Actuellement 3 puzzles par jeu — destinés à grandir via le pipeline

### Variables d'environnement
Aucune — projet 100% local et statique.

### Ce qu'il NE FAUT PAS faire
- Ne pas scraper LinkedIn directement (contrainte explicite README)
- Ne pas republier les grilles extraites ni les puzzles complets
- Ne pas découper App.tsx sans plan clair (refactoring non prioritaire)
- Ne pas ajouter de dépendances backend (ex: base de données) — les puzzles sont des fichiers JSON
- Ne pas mélanger le code Python du solver et le code React

## Commandes utiles

```bash
# Backend Python
source .venv/bin/activate
lgs --help                    # CLI principal
pytest -q                     # Tests (aucun actuellement)
ruff check src/               # Lint

# Frontend Web
cd web
npm run dev                   # Dev server (Vite)
npm run build                 # Build production
npm run preview               # Preview build

# Pipeline extraction
export PLAYLIST_URL="https://www.youtube.com/playlist?list=..."
bash scripts/01_download_playlist.sh --playlist-url "$PLAYLIST_URL"
python scripts/02_extract_frames.py
# ... scripts 03→07
```
