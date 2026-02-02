"""Build zip_unique.json and realign zip_runs.jsonl puzzle ids."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PuzzleEntry:
    key: str
    source: str
    payload: dict


def _load_puzzle(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "n": data["n"],
        "numbers": data.get("numbers", []),
        "walls": data.get("walls", []),
    }


def _collect_puzzles(base: Path, source: str) -> list[PuzzleEntry]:
    if not base.exists():
        return []

    entries: list[PuzzleEntry] = []
    for path in sorted(base.rglob("*.json")):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if rel.parts[0].startswith("size_"):
            key = f"{rel.parts[0]}/{path.stem}"
        else:
            key = path.stem
        entries.append(PuzzleEntry(key=key, source=source, payload=_load_puzzle(path)))
    return entries


def build_zip_unique(curated_dir: Path, generated_dir: Path) -> tuple[list[dict], dict[str, dict]]:
    puzzles = []
    puzzles.extend(_collect_puzzles(curated_dir, "imported"))
    puzzles.extend(_collect_puzzles(generated_dir, "generated"))

    seen: set[str] = set()
    unique_entries: list[PuzzleEntry] = []
    for entry in puzzles:
        if entry.key in seen:
            continue
        seen.add(entry.key)
        unique_entries.append(entry)

    unique_entries.sort(key=lambda item: (item.source, item.key))

    output: list[dict] = []
    index: dict[str, dict] = {}
    for idx, entry in enumerate(unique_entries, start=1):
        payload = {
            "id": idx,
            "source": entry.source,
            **entry.payload,
        }
        output.append(payload)
        index[entry.key] = payload
    return output, index


def update_runs(runs_path: Path, puzzle_index: dict[str, dict]) -> None:
    rows = []
    missing: set[str] = set()
    for line in runs_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = row.get("puzzle_id")
        if key not in puzzle_index:
            missing.add(str(key))
            rows.append(row)
            continue
        entry = puzzle_index[key]
        row["puzzle_id"] = entry["id"]
        row["source"] = entry["source"]
        rows.append(row)

    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Missing puzzles for puzzle_id: {missing_list}")

    runs_path.write_text("\n".join(json.dumps(row, separators=(",", ":")) for row in rows) + "\n", encoding="utf-8")


def main() -> None:
    curated_dir = Path("data/curated/zip")
    generated_dir = Path("data/generated/zip")
    runs_path = Path("data/benchmarks/zip_runs.jsonl")
    output_path = Path("data/zip_unique.json")

    puzzles, index = build_zip_unique(curated_dir, generated_dir)
    output_path.write_text(
        json.dumps({"game": "zip", "version": 1, "puzzles": puzzles}, indent=2),
        encoding="utf-8",
    )

    update_runs(runs_path, index)


if __name__ == "__main__":
    main()
