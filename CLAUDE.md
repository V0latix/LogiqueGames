# CLAUDE.md — LinkedIn Games Solver

> Lire `docs/project-context.md` en premier. Ce fichier est le résumé des règles essentielles.

## Activation rapide

```bash
source .venv/bin/activate   # Toujours activer le venv Python
cd web && npm run dev        # Frontend (port 5173)
```

## Règles critiques

### Python
- Package installable : `pip install -e .` depuis la racine
- Chaque jeu dans `src/linkedin_game_solver/games/<game>/` — structure obligatoire : `solver_*.py`, `generator.py`, `parser.py`, `renderer.py`, `validator.py`
- Types partagés dans `core/types.py` — ne pas redéfinir
- Format puzzle JSON : conforme à `spec.md`
- Tests : `pytest` (venv activé) — 27 fichiers, 36 passing, 23 failing (fixtures manquantes dans `data/curated/`)
- Lint : `ruff check src/`

### Frontend
- Tout le code est dans `web/src/App.tsx` (1249 lignes) — ne pas découper sans plan approuvé
- Données statiques : `web/public/data/queens_unique.json` et `zip_unique.json`
- Pas de dépendances UI tierces (pas de shadcn, pas de Tailwind)
- Stats dans `localStorage` (clé `linkedin-games-stats`)
- `strict: true` TypeScript, imports relatifs

## Ce qu'il NE FAUT PAS faire
- Ne pas scraper LinkedIn directement
- Ne pas republier les grilles extraites ni les puzzles complets
- Ne pas ajouter de backend ou base de données
- Ne pas mélanger code Python solver et code React
- Ne pas découper `App.tsx` sans plan de refactoring approuvé

## Artifacts BMAD
- `docs/project-context.md` — constitution complète du projet (lire en premier)
- `docs/architecture.md` — architecture détaillée
- `docs/prd.md` — PRD et backlog
- `docs/epic-*.md` — épics
- `docs/stories/` — stories ready for dev
