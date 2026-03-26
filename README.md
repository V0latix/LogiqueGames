# Zip (LinkedIn Games) - Video Frame Extraction Pipeline

Pipeline reproductible pour extraire des grilles **Zip** depuis une playlist YouTube (frames vidéo), sans scraping LinkedIn.

## Scope et contraintes

- Source unique: **vidéo YouTube** (pas de scraping LinkedIn).
- Usage attendu: perso / recherche / solver.
- V1 = MVP robuste (pas d'extraction parfaite garantie).
- Ne pas republier les images extraites ni les puzzles complets.

## Arborescence

```text
.
├── scripts/
│   ├── config.py
│   ├── pipeline_utils.py
│   ├── 00_setup_check.py
│   ├── 01_download_playlist.sh
│   ├── 02_extract_frames.py
│   ├── 03_pick_best_frames.py
│   ├── 04_crop_deskew_grid.py
│   ├── 05_export_archive.py
│   ├── 06_grids_to_zip_puzzles.py
│   ├── 07_export_site_zip_format.py
│   └── smoke_test_pipeline.py
├── zip_archive/
│   ├── raw_videos/
│   ├── frames/
│   ├── candidates/
│   ├── grids/
│   └── metadata/
├── requirements.txt
└── .gitignore
```

## Prérequis

- Python 3.11+
- `yt-dlp`
- `ffmpeg` (incluant `ffprobe`)
- dépendances Python dans `requirements.txt`

### Installation macOS

```bash
brew install yt-dlp ffmpeg
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/00_setup_check.py
```

### Installation Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install -y ffmpeg yt-dlp python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/00_setup_check.py
```

## Run complet (5 commandes)

Définir la playlist:

```bash
export PLAYLIST_URL="https://www.youtube.com/playlist?list=..."
```

1. Télécharger la playlist

```bash
bash scripts/01_download_playlist.sh --playlist-url "$PLAYLIST_URL" --limit 10
```

2. Extraire les frames

```bash
python scripts/02_extract_frames.py --playlist-url "$PLAYLIST_URL" --fps 0.5 --limit 10 --start_offset 2 --end_offset 2
```

3. Sélectionner la meilleure frame

```bash
python scripts/03_pick_best_frames.py --limit 10 --top-k 5
```

4. Crop + deskew de la grille

```bash
python scripts/04_crop_deskew_grid.py --limit 10
```

5. Export index + bundle

```bash
python scripts/05_export_archive.py
```

## CLI disponibles

```bash
python scripts/02_extract_frames.py --playlist-url ... --fps 0.5 --limit 10
python scripts/03_pick_best_frames.py --limit 10 --top-k 5
python scripts/04_crop_deskew_grid.py --limit 10
python scripts/05_export_archive.py
```

## Sorties

- Grilles rectifiées: `zip_archive/grids/*_grid.png`
- Index principal: `zip_archive/metadata/index.json`
- Galerie revue: `zip_archive/metadata/gallery.html`
- Bundle zip: `zip_archive/metadata/zip_archive_bundle.zip`
- Conversion JSON (format puzzle Zip du repo): `zip_archive/puzzles_zip/*.json`
- Manifest de conversion JSON: `zip_archive/metadata/puzzles_zip_manifest.json`

Le fichier `index.json` contient:

- `video_id`, `title`, `playlist_index`, `source_url`
- `frame_timestamp`
- `paths` (raw video / chosen frame / grid image)
- `status` (`ok` ou `needs_review`)

## Revue manuelle (`needs_review`)

1. Ouvrir les candidates d'une vidéo:
   - `zip_archive/candidates/<video_basename>/candidate_XX_frame_XXXXXX.png`
2. Choisir une meilleure frame.
3. Relancer le crop sur cette vidéo avec override:

```bash
python scripts/04_crop_deskew_grid.py \
  --only-video <video_basename> \
  --override-frame zip_archive/candidates/<video_basename>/candidate_02_frame_000123.png \
  --force
```

4. Réexporter l'index:

```bash
python scripts/05_export_archive.py --force
```

## Conversion PNG -> format puzzle Zip (JSON)

Convertit chaque `grid.png` en puzzle JSON compatible parser Zip:

```bash
python scripts/06_grids_to_zip_puzzles.py --force
```

Entrées / sorties:
- entrée: `zip_archive/metadata/index.json` + `zip_archive/grids/*.png`
- sortie JSON: `zip_archive/puzzles_zip/#xxx_YYYY-MM-DD__*.json`
- manifeste qualité: `zip_archive/metadata/puzzles_zip_manifest.json`
- archive zip JSON: `zip_archive/metadata/puzzles_zip_bundle.zip`

## Export format exact site

Produit un JSON strictement compatible avec `web/public/data/zip_unique.json`:

```bash
python scripts/07_export_site_zip_format.py
```

Sorties:
- JSON: `zip_archive/metadata/zip_site_format.json`
- ZIP prêt à déposer côté site: `zip_archive/metadata/zip_site_format_bundle.zip` (contient `data/zip_unique.json`)

## Ajuster les seuils heuristiques

Les constantes sont dans `scripts/config.py`:

- `TARGET_WIDTH`
- `CANNY_LOW`, `CANNY_HIGH`
- `HOUGH_THRESHOLD`, `HOUGH_MIN_LINE_LENGTH`, `HOUGH_MAX_LINE_GAP`
- `BLUR_THRESHOLD`
- `GRID_SCORE_MIN`
- `MORPH_CLOSE_KERNEL`, `MORPH_OPEN_KERNEL`

## Idempotence et reprise

- Les scripts sautent les sorties déjà présentes.
- Ajouter `--force` pour recalculer.
- Les erreurs sont gérées par vidéo (le batch continue).

## Smoke test rapide (optionnel)

Si une vidéo existe déjà dans `zip_archive/raw_videos`:

```bash
python scripts/smoke_test_pipeline.py --fps 0.5
```

## Remarques

- `01_download_playlist.sh` conserve l'ordre de playlist dans les noms:
  `%(playlist_index)03d_%(id)s_%(title)s.%(ext)s`
- Le traitement d'image est sans OCR par défaut.
- Un hook OCR pourra être ajouté plus tard si besoin.
