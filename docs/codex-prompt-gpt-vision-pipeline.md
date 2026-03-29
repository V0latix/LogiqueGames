# Codex Prompt — Pipeline GPT Vision pour extraction de puzzles LinkedIn

## Contexte du projet

Ce projet (`linkedin-game-solver`) extrait des puzzles LinkedIn (Queens et Zip) depuis des vidéos YouTube et les convertit en JSON pour un frontend React.

### Pipeline actuel (scripts numérotés dans `scripts/`)

```
01_download_playlist.sh     → télécharge les vidéos
02_extract_frames.py        → extrait des frames PNG depuis chaque vidéo
03_pick_best_frames.py      → choisit la meilleure frame par vidéo
                               → output: zip_archive/candidates/<basename>/chosen_frame.png
                               → manifest: zip_archive/metadata/selected_frames.json
04_crop_deskew_grid.py      → recadre/deskew la grille (CV2)
                               → output: zip_archive/grids/<basename>/grid.png
                               → manifest: zip_archive/metadata/grid_results.json
05_export_archive.py        → consolide les métadonnées
                               → output: zip_archive/metadata/index.json
06_grids_to_queens_puzzles.py  → CV2 color clustering → JSON queens (souvent mauvais)
06_grids_to_zip_puzzles.py     → CV2 circle detection + KNN → JSON zip (souvent mauvais)
07_export_site_queens_format.py / 07_export_site_zip_format.py
                               → formate pour le site web
```

### Problème

Les scripts 04 + 06 (recadrage par CV2 et OCR/color-clustering) produisent des résultats incorrects. L'extraction des régions Queens (clustering couleur k-means) et des numéros Zip (KNN sur digits) échoue souvent.

### Solution

Créer un nouveau script `scripts/06b_gpt_vision_puzzles.py` qui remplace les étapes 04→06 en envoyant **directement la `chosen_frame.png`** (meilleure frame sélectionnée par le script 03) à un modèle GPT avec vision, et qui parse la réponse JSON pour produire le puzzle dans le bon format.

---

## Ce qu'il faut implémenter

### Fichier à créer : `scripts/06b_gpt_vision_puzzles.py`

**Dépendances** : `openai` (déjà dans le projet ou à ajouter via `pip install openai`).

---

## Formats JSON cibles (source de vérité)

### Queens

```json
{
  "game": "queens",
  "n": 8,
  "regions": [
    [0, 0, 1, 1, 2, 2, 3, 3],
    [0, 0, 1, 1, 2, 2, 3, 3],
    ...
  ],
  "givens": {
    "queens": [],
    "blocked": []
  },
  "meta": {
    "video_id": "...",
    "playlist_index": 1,
    "puzzle_number": 668,
    "puzzle_date": "2026-02-27",
    "source_url": "...",
    "frame_timestamp": "00:00:05",
    "grid_image": "zip_archive/candidates/.../chosen_frame.png",
    "name": "Queens #668 - 2026-02-27",
    "conversion": "gpt_vision_v1"
  }
}
```

- `n` : taille de la grille (n×n, typiquement 7-11)
- `regions` : matrice n×n d'entiers 0-indexés, un entier par région colorée. Les cases de la même couleur ont le même entier. Les IDs doivent être assignés en ordre de lecture (première occurrence haut-gauche → bas-droite, region 0 = première couleur rencontrée).
- `givens.queens` / `givens.blocked` : laisser vide `[]` (pas de givens identifiés par vision)

### Zip

```json
{
  "game": "zip",
  "n": 6,
  "numbers": [
    {"k": 1, "r": 2, "c": 3},
    {"k": 2, "r": 0, "c": 1},
    ...
  ],
  "walls": [
    {"r1": 0, "c1": 0, "r2": 0, "c2": 1},
    {"r1": 1, "c1": 2, "r2": 2, "c2": 2},
    ...
  ],
  "meta": {
    "video_id": "...",
    "playlist_index": 1,
    "puzzle_number": 42,
    "puzzle_date": "2026-01-15",
    "source_url": "...",
    "frame_timestamp": "00:00:05",
    "grid_image": "zip_archive/candidates/.../chosen_frame.png",
    "conversion": "gpt_vision_v1"
  }
}
```

- `n` : taille de la grille (n×n)
- `numbers` : checkpoints numérotés. `k` = numéro (1 à N), `r` = ligne (0-indexée), `c` = colonne (0-indexée)
- `walls` : murs épais entre deux cellules adjacentes. `(r1,c1)` et `(r2,c2)` sont les deux cellules de part et d'autre du mur. Deux cellules adjacentes : soit même ligne colonnes consécutives, soit même colonne lignes consécutives.

---

## Prompts GPT Vision

### Prompt système (commun aux deux jeux)

```
You are an expert puzzle extractor for LinkedIn games. You receive a screenshot of a LinkedIn puzzle (either Queens or Zip) and must return a valid JSON object describing the puzzle. Return ONLY valid JSON, no explanation, no markdown code block, just raw JSON.
```

### Prompt utilisateur pour **Queens**

```
This is a Queens puzzle screenshot from LinkedIn.

The grid is n×n. Each cell belongs to exactly one colored region. There are n distinct colors/regions.

Return a JSON object with this exact schema:
{
  "game": "queens",
  "n": <integer, grid size>,
  "regions": [
    [<region_id for row 0>, ...],
    [<region_id for row 1>, ...],
    ...
  ]
}

Rules:
- regions is an n×n matrix of integers (0-indexed)
- Region IDs are assigned in reading order: the first color encountered (top-left to bottom-right) gets ID 0, the next new color gets ID 1, etc.
- Every cell in the same colored area must have the same region ID
- Each region ID must appear at least once
- IDs must be consecutive integers from 0 to n-1

Return ONLY the JSON object, no markdown, no explanation.
```

### Prompt utilisateur pour **Zip**

```
This is a Zip puzzle screenshot from LinkedIn.

The grid is n×n. It contains:
1. Numbered circles (checkpoints): black circles with a white number inside, from 1 to some maximum K
2. Thick walls: bold/thick borders between some adjacent cells (NOT the outer border)

Return a JSON object with this exact schema:
{
  "game": "zip",
  "n": <integer, grid size>,
  "numbers": [
    {"k": <number>, "r": <row 0-indexed>, "c": <col 0-indexed>},
    ...
  ],
  "walls": [
    {"r1": <row>, "c1": <col>, "r2": <row>, "c2": <col>},
    ...
  ]
}

Rules:
- numbers: list all numbered circles, sorted by k ascending
- walls: each wall entry has (r1,c1) and (r2,c2) being the two adjacent cells on either side of a thick interior wall. Adjacent means same row with consecutive columns, or same column with consecutive rows. Do NOT include the outer border of the grid.
- rows and columns are 0-indexed (top-left is r=0, c=0)

Return ONLY the JSON object, no markdown, no explanation.
```

### Prompt utilisateur pour **auto-détection** (si le type de jeu n'est pas connu)

```
This is a LinkedIn puzzle screenshot. First identify if it's a Queens puzzle (colored regions, no numbers in cells) or a Zip puzzle (numbered circles and thick walls).

Then extract the puzzle and return a JSON object.

For Queens, return:
{"game": "queens", "n": <int>, "regions": [[...], ...]}

For Zip, return:
{"game": "zip", "n": <int>, "numbers": [{"k":..,"r":..,"c":..},...], "walls": [{"r1":..,"c1":..,"r2":..,"c2":..},...]}

Return ONLY the JSON object.
```

---

## Spécification du script `scripts/06b_gpt_vision_puzzles.py`

### Interface CLI

```
python scripts/06b_gpt_vision_puzzles.py [OPTIONS]

Options:
  --selection-metadata   Path to selected_frames.json
                         (default: zip_archive/metadata/selected_frames.json)
  --index                Path to index.json (alternative source, used si
                         selection-metadata n'a pas de chosen_frame)
                         (default: zip_archive/metadata/index.json)
  --out-dir              Output directory for puzzle JSON files
                         (default: zip_archive/puzzles_gpt)
  --manifest             Output manifest path
                         (default: zip_archive/metadata/puzzles_gpt_manifest.json)
  --game                 Force game type: "queens", "zip", or "auto" (default: auto)
  --model                OpenAI model to use (default: gpt-4.1)
  --limit                Process only the first N entries
  --force                Overwrite existing output files
  --verbose              Print per-entry status
  --only-video           Process only a specific video_basename
  --api-key              OpenAI API key (default: reads OPENAI_API_KEY env var)
```

### Comportement attendu

1. **Lire les entrées** depuis `--selection-metadata` (champ `videos` avec `status == "ok"` et `chosen_frame` non-null). Si une entrée a un `chosen_frame`, l'utiliser comme image source. Sinon, essayer le champ `paths.grid_image` depuis `--index`.

2. **Pour chaque entrée** :
   a. Lire l'image source (chosen_frame.png ou grid_image)
   b. Encoder en base64
   c. Appeler l'API OpenAI vision avec le bon prompt (selon `--game`)
   d. Parser le JSON retourné (gérer les erreurs de parse gracieusement)
   e. Valider la structure minimale (présence de `game`, `n`, `regions` ou `numbers`)
   f. Enrichir avec les métadonnées de l'entrée (video_id, puzzle_number, etc.)
   g. Sauvegarder dans `--out-dir/<filename>.json`

3. **Nommage des fichiers output** : même convention que les scripts 06 existants :
   ```
   #{puzzle_number:03d}_{puzzle_date}__{video_basename}.json
   ```
   Si puzzle_number ou puzzle_date est absent : `#unknown_date_unknown__{basename}.json`

4. **Status** de chaque entrée :
   - `"ok"` : JSON parsé et validé avec succès
   - `"needs_review"` : erreur API, JSON invalide, validation échouée, ou image introuvable

5. **Manifest output** (même structure que les manifests existants) :
   ```json
   {
     "generated_at": "<ISO datetime>",
     "model": "<model name>",
     "game": "<queens|zip|auto>",
     "count": N,
     "ok": K,
     "needs_review": M,
     "entries": [
       {
         "video_basename": "...",
         "playlist_index": 1,
         "video_id": "...",
         "puzzle_number": 42,
         "puzzle_date": "2026-01-15",
         "grid_image": "zip_archive/candidates/.../chosen_frame.png",
         "json_path": "zip_archive/puzzles_gpt/#042_2026-01-15__basename.json",
         "n": 8,
         "status": "ok",
         "error": null
       }
     ]
   }
   ```

6. **Skip si déjà existant** : si le fichier output existe déjà et `--force` n'est pas passé, skip et marquer `"skipped": true`.

### Gestion des erreurs

- Si l'API retourne du markdown (```json ... ```), l'extraire proprement avant de parser
- Si le JSON est invalide : `status = "needs_review"`, `error = "invalid json: <message>"`
- Si l'image n'existe pas : `status = "needs_review"`, `error = "image not found: <path>"`
- Si l'API rate-limit : retry avec backoff exponentiel (max 3 tentatives, délais 5s, 15s, 30s)
- Si la validation échoue (ex: `len(regions) != n`) : `status = "needs_review"`, `error = "validation: <detail>"`

### Validation minimale des puzzles

**Queens** :
```python
assert payload["game"] == "queens"
assert isinstance(payload["n"], int) and 4 <= payload["n"] <= 15
regions = payload["regions"]
assert len(regions) == payload["n"]
assert all(len(row) == payload["n"] for row in regions)
# region IDs doivent être 0 à n-1
```

**Zip** :
```python
assert payload["game"] == "zip"
assert isinstance(payload["n"], int) and 3 <= payload["n"] <= 15
numbers = payload["numbers"]
assert len(numbers) >= 2
assert all("k" in x and "r" in x and "c" in x for x in numbers)
# k doit être unique, r et c dans [0, n-1]
```

---

## Structure des appels OpenAI

```python
from openai import OpenAI
import base64

client = OpenAI(api_key=api_key)

with open(image_path, "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}",
                        "detail": "high"
                    }
                },
                {
                    "type": "text",
                    "text": user_prompt
                }
            ]
        }
    ],
    max_tokens=4096,
    temperature=0,
)

raw = response.choices[0].message.content.strip()
```

---

## Intégration dans le pipeline

Après l'implémentation, le pipeline complet devient :

```bash
# Étapes 01-03 inchangées
bash scripts/01_download_playlist.sh --playlist-url "$PLAYLIST_URL"
python scripts/02_extract_frames.py
python scripts/03_pick_best_frames.py

# Nouvelle étape : remplace 04 + 06
export OPENAI_API_KEY="sk-..."
python scripts/06b_gpt_vision_puzzles.py \
  --game auto \
  --model gpt-4.1 \
  --verbose

# Étapes 05 et 07 : à adapter pour lire depuis puzzles_gpt/ au lieu de puzzles_queens/ et puzzles_zip/
# OU : utiliser les fichiers JSON de puzzles_gpt/ directement dans les exports site
```

### Adaptation du script 07 (export site)

Le script `07_export_site_queens_format.py` existant lit depuis `zip_archive/puzzles_queens/`. Il faudra soit :
- Ajouter un argument `--manifest` pointant vers `puzzles_gpt_manifest.json` dans le script 07
- Ou créer un nouveau script `07b_export_site_from_gpt.py` qui lit `puzzles_gpt_manifest.json` et produit le même format que les scripts 07 existants

Le format site final (`web/public/data/queens_unique.json` / `zip_unique.json`) doit rester identique :

**Queens site format** :
```json
{
  "game": "queens",
  "version": 1,
  "puzzles": [
    {
      "id": 1,
      "source": "youtube_extracted",
      "n": 8,
      "regions": [[0,0,1,1,...], ...],
      "givens": {"queens": [], "blocked": []},
      "name": "Queens #668 - 2026-02-27"
    }
  ]
}
```

**Zip site format** :
```json
{
  "game": "zip",
  "version": 1,
  "puzzles": [
    {
      "id": 1,
      "source": "youtube_extracted",
      "n": 6,
      "numbers": [{"k":1,"r":2,"c":3}, ...],
      "walls": [{"r1":0,"c1":0,"r2":0,"c2":1}, ...]
    }
  ]
}
```

---

## Conventions de code à respecter

Le projet utilise ces patterns dans tous les scripts — les respecter :

```python
from pipeline_utils import dump_json, ensure_dir, load_json, relative_to_cwd, utc_now_iso

# dump_json(path, payload) → écrit un JSON indenté (indent=2)
# load_json(path, default={}) → lit un JSON avec fallback
# ensure_dir(path) → mkdir -p sur le parent
# relative_to_cwd(path) → chemin relatif au cwd pour les manifests
# utc_now_iso() → timestamp ISO UTC pour "generated_at"
```

Les paths dans les manifests sont **relatifs au cwd** (via `relative_to_cwd()`).

Les chemins absolus sont résolus ainsi :
```python
path = Path(value)
if not path.is_absolute():
    path = Path.cwd() / path
```

---

## Tests à écrire

Créer `tests/test_06b_gpt_vision.py` avec des tests unitaires pour :

1. **`test_parse_gpt_response_clean_json`** : JSON propre → parsing OK
2. **`test_parse_gpt_response_with_markdown_fences`** : JSON enrobé dans ```json ... ``` → extrait correctement
3. **`test_validate_queens_ok`** : payload Queens valide → validation OK
4. **`test_validate_queens_wrong_n`** : `len(regions) != n` → validation échoue
5. **`test_validate_zip_ok`** : payload Zip valide → validation OK
6. **`test_validate_zip_missing_k`** : number sans `k` → validation échoue
7. **`test_output_filename`** : nommage des fichiers output

Ne pas appeler l'API OpenAI dans les tests (mocker `openai.OpenAI`).

---

## Checklist de livraison

- [ ] `scripts/06b_gpt_vision_puzzles.py` créé et fonctionnel
- [ ] `pip install openai` documenté (ou ajouté à `pyproject.toml` / `requirements*.txt` existants)
- [ ] La variable `OPENAI_API_KEY` est lue depuis l'environnement (ne jamais la hardcoder)
- [ ] `tests/test_06b_gpt_vision.py` avec les 7 tests ci-dessus
- [ ] Testé manuellement sur 2-3 images : `python scripts/06b_gpt_vision_puzzles.py --limit 3 --verbose`
- [ ] Le manifest output `puzzles_gpt_manifest.json` est conforme au format décrit
- [ ] Les fichiers JSON individuels dans `puzzles_gpt/` sont conformes aux formats Queens/Zip
