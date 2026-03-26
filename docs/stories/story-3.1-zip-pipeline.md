# Story 3.1 — Pipeline Zip : extraction 50+ puzzles
> Epic : Epic 3 — Croissance du dataset
> Statut : Backlog
> Priorité : Moyenne

## Description
Exécuter le pipeline complet (scripts 01→07) sur une playlist Zip de 50+ vidéos pour peupler `data/curated/zip/` avec 40+ puzzles valides.

## Acceptance Criteria
- [ ] Pipeline exécuté sur 50+ vidéos
- [ ] 40+ puzzles Zip JSON valides générés dans `data/curated/zip/`
- [ ] Chaque puzzle passe le validator Zip
- [ ] `web/public/data/zip_unique.json` mis à jour avec les nouveaux puzzles

## Commandes
```bash
export PLAYLIST_URL="..."
bash scripts/01_download_playlist.sh --playlist-url "$PLAYLIST_URL"
python scripts/02_extract_frames.py
python scripts/03_pick_best_frames.py
python scripts/04_crop_deskew_grid.py
python scripts/05_export_archive.py
python scripts/06_grids_to_zip_puzzles.py
python scripts/07_export_site_zip_format.py
```
