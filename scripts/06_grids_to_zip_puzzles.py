#!/usr/bin/env python3
"""Convert extracted Zip grid PNGs into JSON puzzles compatible with the repo Zip format."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

import cv2
import numpy as np
from config import TARGET_WIDTH
from extraction_common import candidate_frame_paths, normalize_grid_from_frame, resolve_path
from pipeline_utils import dump_json, ensure_dir, load_json, relative_to_cwd, utc_now_iso

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from linkedin_game_solver.games.zip.parser import parse_puzzle_dict
from linkedin_game_solver.games.zip.solver_forced import solve_forced


@dataclass
class Circle:
    x: float
    y: float
    r: float


@dataclass
class ZipHypothesis:
    payload: dict
    n: int
    numbers: list[dict[str, int]]
    walls: list[dict[str, int]]
    recognition_confidence: float
    parse_ok: bool
    solver_ok: bool
    score: float
    frame_path: Path
    normalization_method: str
    quad_area_ratio: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert grid PNGs to Zip JSON puzzles")
    parser.add_argument("--index", default="zip_archive/metadata/index.json")
    parser.add_argument("--out-dir", default="zip_archive/puzzles_zip")
    parser.add_argument("--manifest", default="zip_archive/metadata/puzzles_zip_manifest.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-video", default=None, help="Process only a specific video_basename")
    parser.add_argument("--candidate-frames-max", type=int, default=20)
    parser.add_argument("--candidate-consensus", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--target-width", type=int, default=TARGET_WIDTH)
    parser.add_argument("--min-quad-area-ratio", type=float, default=0.08)
    parser.add_argument("--solver-time-limit-s", type=float, default=0.2)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def cluster_positions(values: list[float], eps: float = 8.0) -> list[float]:
    if not values:
        return []
    values = sorted(values)
    clusters: list[list[float]] = []
    for value in values:
        if not clusters or abs(value - clusters[-1][-1]) > eps:
            clusters.append([value])
        else:
            clusters[-1].append(value)
    return [float(sum(cluster) / len(cluster)) for cluster in clusters]


def _smooth_1d(values: np.ndarray, k: int = 9) -> np.ndarray:
    if k <= 1:
        return values
    k = int(k)
    if k % 2 == 0:
        k += 1
    kernel = np.ones(k, dtype=np.float32) / float(k)
    return np.convolve(values.astype(np.float32), kernel, mode="same")


def _runs_to_centers(indices: np.ndarray, max_gap: int = 2) -> list[float]:
    if indices.size == 0:
        return []
    runs: list[list[int]] = []
    current = [int(indices[0])]
    for idx in indices[1:]:
        idx = int(idx)
        if idx - current[-1] <= max_gap:
            current.append(idx)
        else:
            runs.append(current)
            current = [idx]
    runs.append(current)
    return [float(sum(run) / len(run)) for run in runs]


def _detect_grid_lines_projection(gray: np.ndarray) -> tuple[list[float], list[float]]:
    # Grid lines (and walls) are darker than the board background.
    # Use an adaptive threshold so we don't include tinted cell backgrounds
    # (eg. blue boards), which would flatten the projection signal.
    p15 = float(np.percentile(gray, 15))
    p50 = float(np.percentile(gray, 50))
    thr = min(p15 + 5.0, p50 - 5.0)
    thr = float(max(40.0, min(245.0, thr)))
    mask = (gray < thr).astype(np.float32)
    v = mask.mean(axis=0)
    h = mask.mean(axis=1)

    v = _smooth_1d(v, k=11)
    h = _smooth_1d(h, k=11)

    def _threshold(arr: np.ndarray) -> float:
        base = float(np.percentile(arr, 50))
        top = float(np.percentile(arr, 95))
        return base + 0.35 * max(0.0, top - base)

    v_idx = np.where(v > _threshold(v))[0]
    h_idx = np.where(h > _threshold(h))[0]

    xs = cluster_positions(_runs_to_centers(v_idx), eps=7.0)
    ys = cluster_positions(_runs_to_centers(h_idx), eps=7.0)

    h_img, w_img = gray.shape[:2]
    xs = regularize_line_spacing(xs, axis_limit=w_img)
    ys = regularize_line_spacing(ys, axis_limit=h_img)
    return xs, ys


def detect_grid_lines(gray: np.ndarray) -> tuple[list[float], list[float]]:
    def _best_uniform_window(lines: list[float], m: int, desired_span: float | None = None) -> list[float]:
        if len(lines) <= m:
            return lines
        lines = sorted(lines)
        best_window = lines[:m]
        best_score = float("inf")
        for start in range(0, len(lines) - m + 1):
            window = lines[start : start + m]
            gaps = [b - a for a, b in zip(window[:-1], window[1:])]
            if not gaps:
                continue
            # Prefer windows with the most regular spacing (grid lines).
            std = float(np.std(np.array(gaps, dtype=np.float32)))
            span = float(window[-1] - window[0])
            # Regular spacing is important, but pick the window that also spans
            # the largest region (to avoid UI separators).
            score = std / max(1.0, span)
            if desired_span is not None and desired_span > 1.0:
                score += 0.35 * (abs(span - desired_span) / desired_span)
            if score < best_score:
                best_score = score
                best_window = window
        return best_window

    def _trim_to_square(xs: list[float], ys: list[float]) -> tuple[list[float], list[float]]:
        m = min(len(xs), len(ys))
        if m < 3:
            return xs, ys

        xs_sorted = sorted(xs)
        ys_sorted = sorted(ys)

        if len(xs_sorted) < len(ys_sorted) and len(xs_sorted) >= 2:
            desired = float(xs_sorted[m - 1] - xs_sorted[0])
            return xs_sorted[:m], _best_uniform_window(ys_sorted, m, desired_span=desired)

        if len(ys_sorted) < len(xs_sorted) and len(ys_sorted) >= 2:
            desired = float(ys_sorted[m - 1] - ys_sorted[0])
            return _best_uniform_window(xs_sorted, m, desired_span=desired), ys_sorted[:m]

        # Same count: still trim to the best window for uniformity.
        return _best_uniform_window(xs_sorted, m), _best_uniform_window(ys_sorted, m)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)

    h, w = gray.shape[:2]
    all_h: list[float] = []
    all_v: list[float] = []

    for threshold in (25, 35, 45, 55):
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=threshold,
            minLineLength=60,
            maxLineGap=4,
        )
        if lines is None:
            continue

        for line in lines[:, 0]:
            x1, y1, x2, y2 = line
            angle = abs(np.degrees(np.arctan2((y2 - y1), (x2 - x1))))
            angle = min(angle, 180.0 - angle)
            if angle < 8:
                all_h.append((y1 + y2) / 2.0)
            elif angle > 82:
                all_v.append((x1 + x2) / 2.0)

    ys = cluster_positions(all_h, eps=7.0)
    xs = cluster_positions(all_v, eps=7.0)

    xs = regularize_line_spacing(xs, axis_limit=w)
    ys = regularize_line_spacing(ys, axis_limit=h)

    # If Hough is weak (few lines), fall back to a projection-based method which
    # tends to work better with thick walls and UI artefacts.
    xs2, ys2 = _detect_grid_lines_projection(gray)
    if min(len(xs2), len(ys2)) > min(len(xs), len(ys)):
        xs, ys = xs2, ys2

    # Some crops include UI elements that generate extra "lines" in one axis.
    # The Zip grid is square, so trim the denser axis down to the best uniform window.
    xs, ys = _trim_to_square(xs, ys)
    return xs, ys


def regularize_line_spacing(lines: list[float], axis_limit: int) -> list[float]:
    if len(lines) < 3:
        return lines

    lines = sorted(lines)
    gaps = [b - a for a, b in zip(lines[:-1], lines[1:]) if 35 <= (b - a) <= 260]
    if not gaps:
        return lines

    step = float(np.median(np.array(gaps, dtype=np.float32)))
    if step <= 10:
        return lines

    # Build a lattice with the dominant step and keep the observed support.
    offset = float(np.median([value % step for value in lines]))
    start = offset
    while start - step >= -0.5 * step:
        start -= step

    lattice: list[float] = []
    value = start
    while value <= axis_limit + 0.5 * step:
        lattice.append(value)
        value += step

    supported = [
        value for value in lattice if any(abs(obs - value) <= 0.35 * step for obs in lines)
    ]
    if len(supported) < 3:
        return lines

    first, last = min(supported), max(supported)
    dense: list[float] = []
    value = first
    while value <= last + 1e-6:
        dense.append(value)
        value += step

    return dense


def _dark_run(arr: np.ndarray, center: int, thresh: int, max_half: int) -> int:
    """Width of the dark run (pixel value <= thresh) centered near `center` in a 1-D array."""
    n = len(arr)
    if n == 0:
        return 0
    center = max(0, min(n - 1, center))

    # Walk up to ±3 px to find a dark pixel if center is not dark.
    if arr[center] > thresh:
        for delta in range(1, 4):
            lo, hi = center - delta, center + delta
            if lo >= 0 and arr[lo] <= thresh:
                center = lo
                break
            if hi < n and arr[hi] <= thresh:
                center = hi
                break
        else:
            return 0

    left = center
    while left > max(0, center - max_half) and arr[left] <= thresh:
        left -= 1
    right = center
    while right < min(n - 1, center + max_half) and arr[right] <= thresh:
        right += 1
    return right - left


def _edge_thickness(
    gray: np.ndarray,
    axis: int,
    line_pos: float,
    span_start: float,
    span_end: float,
    dark_thresh: int = 80,
    n_samples: int = 7,
    max_half: int = 12,
) -> float:
    """Median dark-run thickness for one interior grid edge.

    axis=0: horizontal edge (line_pos is a y-coordinate; profile is vertical).
    axis=1: vertical edge   (line_pos is an x-coordinate; profile is horizontal).
    span_start / span_end delimit the cell extent perpendicular to the edge.
    """
    h, w = gray.shape
    runs: list[int] = []

    for t in np.linspace(0.2, 0.8, n_samples):
        cross = span_start * (1 - t) + span_end * t

        if axis == 0:
            x = max(0, min(w - 1, int(round(cross))))
            yc = int(round(line_pos))
            y0, y1 = max(0, yc - max_half), min(h, yc + max_half + 1)
            profile = gray[y0:y1, x]
            center_in = yc - y0
        else:
            y = max(0, min(h - 1, int(round(cross))))
            xc = int(round(line_pos))
            x0, x1 = max(0, xc - max_half), min(w, xc + max_half + 1)
            profile = gray[y, x0:x1]
            center_in = xc - x0

        runs.append(_dark_run(profile, center_in, dark_thresh, max_half))

    return float(np.median(runs)) if runs else 0.0


def detect_walls(
    gray: np.ndarray,
    xs: list[float],
    ys: list[float],
    n: int,
    dark_thresh: int = 80,
    wall_ratio: float = 2.2,
) -> list[dict]:
    """Detect walls between adjacent cells using line-thickness analysis.

    For every interior edge, measure the perpendicular dark-pixel run width.
    An edge is classified as a wall when its thickness is >= wall_ratio * median
    thickness across all interior edges.

    Returns a sorted list of {"r1", "c1", "r2", "c2"} dicts where (r1,c1) and
    (r2,c2) are the two cells on either side of the wall.
    """
    if len(xs) < 2 or len(ys) < 2 or n < 2:
        return []

    thicknesses: dict[tuple, float] = {}

    # Horizontal edges: interior horizontal lines at ys[1] … ys[n-1]
    for r in range(n - 1):
        y_line = ys[r + 1]
        for c in range(n):
            t = _edge_thickness(gray, 0, y_line, xs[c], xs[c + 1], dark_thresh)
            thicknesses[("h", r, c)] = t

    # Vertical edges: interior vertical lines at xs[1] … xs[n-1]
    for r in range(n):
        for c in range(n - 1):
            x_line = xs[c + 1]
            t = _edge_thickness(gray, 1, x_line, ys[r], ys[r + 1], dark_thresh)
            thicknesses[("v", r, c)] = t

    if not thicknesses:
        return []

    values = np.array(list(thicknesses.values()), dtype=np.float32)
    # Use a low percentile as the baseline "thin grid line" thickness.
    # Median can be dominated by walls when a puzzle has lots of thick edges.
    baseline_t = float(np.percentile(values, 35))
    if baseline_t <= 0:
        return []

    wall_thresh = baseline_t * wall_ratio
    walls: list[dict] = []

    for (axis, r, c), t in thicknesses.items():
        if t < wall_thresh:
            continue
        if axis == "h":
            walls.append({"r1": r, "c1": c, "r2": r + 1, "c2": c})
        else:
            walls.append({"r1": r, "c1": c, "r2": r, "c2": c + 1})

    return sorted(walls, key=lambda w: (w["r1"], w["c1"], w["r2"], w["c2"]))


def detect_circles(gray: np.ndarray) -> list[Circle]:
    # Black circular checkpoints are among the darkest objects, but screenshots vary
    # (blue-tinted boards, compression). Use an adaptive threshold instead of a
    # fixed cutoff so we still pick up slightly lighter "black" circles.
    p3 = float(np.percentile(gray, 3))
    thresh = int(min(95.0, max(55.0, p3 + 35.0)))
    dark = (gray < thresh).astype(np.uint8) * 255
    contours, _ = cv2.findContours(dark, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circles: list[Circle] = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 700 or area > 18000:
            continue

        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            continue
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if circularity < 0.62:
            continue

        (x, y), r = cv2.minEnclosingCircle(contour)
        if r < 12 or r > 80:
            continue
        circles.append(Circle(x=float(x), y=float(y), r=float(r)))

    circles.sort(key=lambda c: (c.y, c.x))
    return circles


def build_digit_knn() -> cv2.ml_KNearest:
    samples: list[np.ndarray] = []
    labels: list[int] = []

    for digit in range(10):
        text = str(digit)
        for font_scale in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3):
            for thickness in (1, 2, 3):
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        img = np.zeros((32, 24), dtype=np.uint8)
                        (tw, th), _ = cv2.getTextSize(
                            text,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale,
                            thickness,
                        )
                        x = max(0, (24 - tw) // 2 + dx)
                        y = max(th + 1, min(31, (32 + th) // 2 + dy))
                        cv2.putText(
                            img,
                            text,
                            (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale,
                            255,
                            thickness,
                            cv2.LINE_AA,
                        )

                        for blur in (False, True):
                            variant = cv2.GaussianBlur(img, (3, 3), 0) if blur else img.copy()
                            _, variant = cv2.threshold(variant, 100, 255, cv2.THRESH_BINARY)
                            variant = cv2.resize(variant, (20, 28), interpolation=cv2.INTER_AREA)
                            samples.append(variant.reshape(-1).astype(np.float32) / 255.0)
                            labels.append(digit)

    knn = cv2.ml.KNearest_create()
    knn.train(np.array(samples, np.float32), cv2.ml.ROW_SAMPLE, np.array(labels, np.int32))
    return knn


def text_patch_from_circle(gray: np.ndarray, circle: Circle) -> np.ndarray:
    x0 = max(0, int(circle.x - circle.r * 0.82))
    x1 = min(gray.shape[1], int(circle.x + circle.r * 0.82))
    y0 = max(0, int(circle.y - circle.r * 0.82))
    y1 = min(gray.shape[0], int(circle.y + circle.r * 0.82))
    roi = gray[y0:y1, x0:x1]

    _, text_mask = cv2.threshold(roi, 155, 255, cv2.THRESH_BINARY)

    h, w = text_mask.shape[:2]
    yy, xx = np.ogrid[:h, :w]
    cx, cy = w / 2.0, h / 2.0
    rr = min(h, w) * 0.49
    circle_mask = ((xx - cx) ** 2 + (yy - cy) ** 2) <= rr * rr
    text_mask = text_mask * circle_mask.astype(np.uint8)

    points = cv2.findNonZero(text_mask)
    out = np.zeros((80, 80), dtype=np.uint8)
    if points is None:
        return out

    x, y, w2, h2 = cv2.boundingRect(points)
    crop = text_mask[y : y + h2, x : x + w2]

    scale = min(70 / max(1, w2), 70 / max(1, h2))
    nw, nh = max(1, int(w2 * scale)), max(1, int(h2 * scale))
    resized = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_AREA)

    ox, oy = (80 - nw) // 2, (80 - nh) // 2
    out[oy : oy + nh, ox : ox + nw] = resized
    return out


def predict_digits_with_knn(text_patch: np.ndarray, knn: cv2.ml_KNearest) -> tuple[int | None, float]:
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(text_patch, connectivity=8)

    boxes: list[tuple[int, int, int, int]] = []
    for idx in range(1, n_labels):
        x, y, w, h, area = stats[idx]
        if area < 20 or h < 8 or w < 3:
            continue
        boxes.append((x, y, w, h))

    if not boxes:
        return None, 0.0

    boxes.sort(key=lambda item: item[0])
    digits: list[str] = []
    confidences: list[float] = []

    for x, y, w, h in boxes:
        patch = text_patch[y : y + h, x : x + w]
        canvas = np.zeros((h + 8, w + 8), dtype=np.uint8)
        canvas[4 : 4 + h, 4 : 4 + w] = patch
        sample_img = cv2.resize(canvas, (20, 28), interpolation=cv2.INTER_AREA)
        sample = sample_img.reshape(1, -1).astype(np.float32) / 255.0

        _ret, result, neighbors, _dist = knn.findNearest(sample, k=5)
        pred = int(result[0, 0])

        neighbor_vals = neighbors.flatten().astype(int).tolist()
        confidence = neighbor_vals.count(pred) / max(1, len(neighbor_vals))

        digits.append(str(pred))
        confidences.append(float(confidence))

    value = int("".join(digits)) if digits else None
    avg_conf = float(sum(confidences) / len(confidences)) if confidences else 0.0
    return value, avg_conf


def number_template(number: int) -> list[np.ndarray]:
    text = str(number)
    templates: list[np.ndarray] = []

    for scale in (0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5):
        for thickness in (2, 3):
            img = np.zeros((80, 80), dtype=np.uint8)
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
            if tw > 74 or th > 74:
                continue
            x = (80 - tw) // 2
            y = (80 + th) // 2
            cv2.putText(
                img,
                text,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                scale,
                255,
                thickness,
                cv2.LINE_AA,
            )
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            templates.append(img)

    return templates


def similarity_to_number(text_patch: np.ndarray, number: int, cache: dict[int, list[np.ndarray]]) -> float:
    templates = cache.setdefault(number, number_template(number))
    if not templates:
        return -1.0
    best = -1.0
    for tmpl in templates:
        score = float(cv2.matchTemplate(text_patch, tmpl, cv2.TM_CCOEFF_NORMED)[0, 0])
        if score > best:
            best = score
    return best


def assign_unique_labels(
    text_patches: list[np.ndarray],
    knn_guesses: list[int | None],
    knn_confidences: list[float],
) -> tuple[list[int], float]:
    def _hungarian_min_cost(cost: list[list[float]]) -> list[int]:
        """Return column assignment for each row (0-indexed) minimizing total cost.

        Implementation: O(n^3) Hungarian algorithm for a square matrix.
        """
        n = len(cost)
        if n == 0:
            return []
        if any(len(row) != n for row in cost):
            raise ValueError("hungarian expects a square cost matrix")

        u = [0.0] * (n + 1)
        v = [0.0] * (n + 1)
        p = [0] * (n + 1)  # matched row for column j
        way = [0] * (n + 1)

        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            minv = [float("inf")] * (n + 1)
            used = [False] * (n + 1)

            while True:
                used[j0] = True
                i0 = p[j0]
                delta = float("inf")
                j1 = 0

                for j in range(1, n + 1):
                    if used[j]:
                        continue
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j

                for j in range(n + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta

                j0 = j1
                if p[j0] == 0:
                    break

            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break

        assignment = [0] * n  # row -> col
        for j in range(1, n + 1):
            assignment[p[j] - 1] = j - 1
        return assignment

    k = len(text_patches)
    available = set(range(1, k + 1))
    cache: dict[int, list[np.ndarray]] = {}
    score_table: list[list[float]] = []

    for i, patch in enumerate(text_patches):
        row: list[float] = []
        for label in range(1, k + 1):
            score = similarity_to_number(patch, label, cache)
            guess = knn_guesses[i]
            conf = knn_confidences[i]
            if guess is not None and label == guess:
                score += 0.20 * conf
            row.append(score)
        score_table.append(row)

    # Global best assignment (greedy can fail when two patches strongly prefer the same label).
    # Hungarian solves the full bipartite matching.
    if k == 0:
        return [], 0.0

    # Convert to a min-cost problem by negating scores.
    cost = [[-score for score in row] for row in score_table]
    row_to_col = _hungarian_min_cost(cost)

    labels = [col + 1 for col in row_to_col]
    picked_scores = [score_table[i][row_to_col[i]] for i in range(k)]
    confidence = float(sum(picked_scores) / len(picked_scores)) if picked_scores else 0.0

    # Keep the original API: list of labels in patch order, plus a confidence proxy.
    # Ensure it's a permutation of 1..k.
    if set(labels) != available:
        # This should never happen for a correct Hungarian assignment,
        # but keep a safe fallback to avoid crashing the pipeline.
        labels = list(range(1, k + 1))
        confidence = 0.0

    return labels, confidence


def infer_cell_index(value: float, lines: list[float], n: int) -> int:
    if not lines:
        return 0
    idx = int(np.searchsorted(np.array(lines, dtype=np.float32), value, side="right") - 1)
    return max(0, min(n - 1, idx))


def _normalize_wall_tuple(wall: dict[str, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    a = (int(wall["r1"]), int(wall["c1"]))
    b = (int(wall["r2"]), int(wall["c2"]))
    return tuple(sorted([a, b]))  # type: ignore[return-value]


def _numbers_signature(numbers: list[dict[str, int]]) -> tuple[tuple[int, int, int], ...]:
    return tuple(sorted((int(n["k"]), int(n["r"]), int(n["c"])) for n in numbers))


def _walls_signature(walls: list[dict[str, int]]) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    return tuple(sorted(_normalize_wall_tuple(wall) for wall in walls))


def _hypothesis_signature(hyp: ZipHypothesis) -> tuple:
    return (int(hyp.n), _numbers_signature(hyp.numbers), _walls_signature(hyp.walls))


def evaluate_zip_constraints(payload: dict, solver_time_limit_s: float = 0.2) -> tuple[bool, bool, list[str]]:
    notes: list[str] = []
    try:
        puzzle = parse_puzzle_dict(payload)
        parse_ok = True
    except Exception as exc:
        parse_ok = False
        notes.append(f"parser_failed:{exc}")
        return parse_ok, False, notes

    try:
        solved = solve_forced(puzzle, time_limit_s=max(0.01, float(solver_time_limit_s)))
        solver_ok = bool(solved.solved)
        if not solver_ok and solved.error:
            notes.append(f"solver_failed:{solved.error}")
    except Exception as exc:
        solver_ok = False
        notes.append(f"solver_exception:{exc}")

    return parse_ok, solver_ok, notes


def pick_consensus_hypothesis(hypotheses: list[ZipHypothesis]) -> tuple[ZipHypothesis, dict]:
    if len(hypotheses) == 1:
        return hypotheses[0], {"mode": "single", "candidates": 1}

    votes: dict[tuple, float] = {}
    by_sig: dict[tuple, list[ZipHypothesis]] = {}
    for hyp in hypotheses:
        sig = _hypothesis_signature(hyp)
        weight = max(0.01, float(hyp.score) + 1.0)
        votes[sig] = votes.get(sig, 0.0) + weight
        by_sig.setdefault(sig, []).append(hyp)

    best_sig = max(
        votes,
        key=lambda sig: (
            votes[sig],
            max(h.score for h in by_sig[sig]),
            len(by_sig[sig]),
        ),
    )
    best_hyp = max(by_sig[best_sig], key=lambda h: h.score)
    return best_hyp, {
        "mode": "consensus",
        "candidates": len(hypotheses),
        "winning_votes": round(votes[best_sig], 5),
        "signature_agreement": len(by_sig[best_sig]),
        "unique_signatures": len(votes),
    }


def output_filename(entry: dict, fallback_idx: int) -> str:
    puzzle_number = entry.get("puzzle_number")
    if isinstance(puzzle_number, int):
        num_part = f"#{puzzle_number:03d}"
    else:
        num_part = "#unknown"
    date_part = str(entry.get("puzzle_date") or "date_unknown")
    basename = str(entry.get("video_basename") or f"video_{fallback_idx:03d}")
    return f"{num_part}_{date_part}__{basename}.json"


def _extract_zip_hypothesis(
    *,
    entry: dict,
    gray: np.ndarray,
    xs: list[float],
    ys: list[float],
    knn: cv2.ml_KNearest,
    frame_path: Path,
    normalization_method: str,
    quad_area_ratio: float,
    solver_time_limit_s: float,
) -> ZipHypothesis | None:
    n = min(len(xs), len(ys)) - 1
    if n < 2:
        return None

    adaptive_dark = int(float(np.percentile(gray, 35)))
    adaptive_dark = max(70, min(170, adaptive_dark))
    walls = detect_walls(gray, xs, ys, n, dark_thresh=adaptive_dark)

    circles = detect_circles(gray)
    if circles and xs and ys:
        cell_w = max(1.0, float(xs[-1] - xs[0]) / max(1, n))
        cell_h = max(1.0, float(ys[-1] - ys[0]) / max(1, n))
        x0f = float(xs[0]) - 0.35 * cell_w
        x1f = float(xs[-1]) + 0.35 * cell_w
        y0f = float(ys[0]) - 0.35 * cell_h
        y1f = float(ys[-1]) + 0.35 * cell_h
        circles = [c for c in circles if x0f <= c.x <= x1f and y0f <= c.y <= y1f]

    if (not circles or len(circles) < 2) and xs and ys:
        cell_w = max(1.0, float(xs[-1] - xs[0]) / max(1, n))
        cell_h = max(1.0, float(ys[-1] - ys[0]) / max(1, n))
        x0 = max(0, int(round(float(xs[0]) - 0.35 * cell_w)))
        x1 = min(gray.shape[1], int(round(float(xs[-1]) + 0.35 * cell_w)))
        y0 = max(0, int(round(float(ys[0]) - 0.35 * cell_h)))
        y1 = min(gray.shape[0], int(round(float(ys[-1]) + 0.35 * cell_h)))
        roi = gray[y0:y1, x0:x1]
        if roi.size:
            roi_blur = cv2.medianBlur(roi, 5)
            min_dist = max(10.0, 0.65 * min(cell_w, cell_h))
            min_r = int(max(8.0, 0.18 * min(cell_w, cell_h)))
            max_r = int(max(min_r + 2.0, 0.48 * min(cell_w, cell_h)))
            found = cv2.HoughCircles(
                roi_blur,
                cv2.HOUGH_GRADIENT,
                dp=1.2,
                minDist=min_dist,
                param1=120,
                param2=22,
                minRadius=min_r,
                maxRadius=max_r,
            )
            if found is not None:
                for x, y, r in found[0]:
                    circles.append(Circle(x=float(x + x0), y=float(y + y0), r=float(r)))
                circles = [c for c in circles if x0 <= c.x <= x1 and y0 <= c.y <= y1]
                circles.sort(key=lambda c: (c.y, c.x))

    if not circles:
        return None

    def _cell_center(row: int, col: int) -> tuple[float, float]:
        cx = (xs[col] + xs[col + 1]) / 2.0 if col + 1 < len(xs) else xs[col]
        cy = (ys[row] + ys[row + 1]) / 2.0 if row + 1 < len(ys) else ys[row]
        return cx, cy

    cell_to_circle: dict[tuple[int, int], Circle] = {}
    for circle in circles:
        row = infer_cell_index(circle.y, ys, n)
        col = infer_cell_index(circle.x, xs, n)
        cell = (row, col)
        if cell not in cell_to_circle:
            cell_to_circle[cell] = circle
        else:
            ccx, ccy = _cell_center(row, col)
            prev = cell_to_circle[cell]
            if (circle.x - ccx) ** 2 + (circle.y - ccy) ** 2 < (prev.x - ccx) ** 2 + (prev.y - ccy) ** 2:
                cell_to_circle[cell] = circle
    circles = sorted(cell_to_circle.values(), key=lambda c: (c.y, c.x))

    patches: list[np.ndarray] = []
    knn_guesses: list[int | None] = []
    knn_confs: list[float] = []
    for circle in circles:
        patch = text_patch_from_circle(gray, circle)
        guess, conf = predict_digits_with_knn(patch, knn)
        patches.append(patch)
        knn_guesses.append(guess)
        knn_confs.append(conf)

    labels, assign_conf = assign_unique_labels(patches, knn_guesses, knn_confs)
    numbers: list[dict[str, int]] = []
    for circle, label in zip(circles, labels):
        row = infer_cell_index(circle.y, ys, n)
        col = infer_cell_index(circle.x, xs, n)
        numbers.append({"k": int(label), "r": int(row), "c": int(col)})
    numbers.sort(key=lambda item: item["k"])

    payload = {
        "game": "zip",
        "n": int(n),
        "numbers": numbers,
        "walls": walls,
        "meta": {
            "video_id": entry.get("video_id"),
            "playlist_index": entry.get("playlist_index"),
            "puzzle_number": entry.get("puzzle_number"),
            "puzzle_date": entry.get("puzzle_date"),
            "source_url": entry.get("source_url"),
            "frame_timestamp": entry.get("frame_timestamp"),
            "grid_image": relative_to_cwd(frame_path),
            "conversion": "png_to_zip_consensus_v2",
            "normalization_method": normalization_method,
        },
    }

    parse_ok, solver_ok, _constraint_notes = evaluate_zip_constraints(payload, solver_time_limit_s=solver_time_limit_s)
    score = (
        float(assign_conf)
        + (0.85 if parse_ok else -0.75)
        + (0.65 if solver_ok else -0.15)
        + min(0.35, float(quad_area_ratio))
    )

    return ZipHypothesis(
        payload=payload,
        n=int(n),
        numbers=numbers,
        walls=walls,
        recognition_confidence=float(assign_conf),
        parse_ok=parse_ok,
        solver_ok=solver_ok,
        score=float(score),
        frame_path=frame_path,
        normalization_method=normalization_method,
        quad_area_ratio=float(quad_area_ratio),
    )


def convert_one(entry: dict, out_dir: Path, knn: cv2.ml_KNearest, args: argparse.Namespace) -> dict:
    file_name = output_filename(entry, fallback_idx=int(entry.get("playlist_index") or 0))
    out_path = out_dir / file_name

    grid_path = resolve_path((entry.get("paths") or {}).get("grid_image") if isinstance(entry.get("paths"), dict) else None)
    if out_path.exists() and not args.force:
        return {
            "video_basename": entry.get("video_basename"),
            "playlist_index": entry.get("playlist_index"),
            "grid_image": relative_to_cwd(grid_path) if grid_path else None,
            "json_path": relative_to_cwd(out_path),
            "status": "ok",
            "skipped": True,
        }

    frame_candidates = candidate_frame_paths(entry, max_frames=int(args.candidate_frames_max))
    if not args.candidate_consensus and frame_candidates:
        frame_candidates = frame_candidates[:1]

    hypotheses: list[ZipHypothesis] = []
    for frame_path in frame_candidates:
        normalized = normalize_grid_from_frame(
            frame_path,
            line_detector=detect_grid_lines,
            target_width=int(args.target_width),
            min_area_ratio=float(args.min_quad_area_ratio),
        )
        if not normalized:
            continue

        hyp = _extract_zip_hypothesis(
            entry=entry,
            gray=normalized["gray"],
            xs=normalized["xs"],
            ys=normalized["ys"],
            knn=knn,
            frame_path=frame_path,
            normalization_method=str(normalized["method"]),
            quad_area_ratio=float(normalized["area_ratio"]),
            solver_time_limit_s=float(args.solver_time_limit_s),
        )
        if hyp is not None:
            hypotheses.append(hyp)

    # Fallback to the legacy pre-cropped grid when frame-based normalization fails.
    if not hypotheses and grid_path and grid_path.exists():
        image = cv2.imread(str(grid_path), cv2.IMREAD_COLOR)
        if image is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            xs, ys = detect_grid_lines(gray)
            hyp = _extract_zip_hypothesis(
                entry=entry,
                gray=gray,
                xs=xs,
                ys=ys,
                knn=knn,
                frame_path=grid_path,
                normalization_method="precomputed_grid",
                quad_area_ratio=0.0,
                solver_time_limit_s=float(args.solver_time_limit_s),
            )
            if hyp is not None:
                hypotheses.append(hyp)

    if not hypotheses:
        return {
            "video_basename": entry.get("video_basename"),
            "playlist_index": entry.get("playlist_index"),
            "grid_image": relative_to_cwd(grid_path) if grid_path else None,
            "status": "needs_review",
            "error": "no valid hypotheses from candidate frames",
        }

    if args.candidate_consensus:
        winner, consensus_info = pick_consensus_hypothesis(hypotheses)
    else:
        winner = max(hypotheses, key=lambda h: h.score)
        consensus_info = {"mode": "best_score_only", "candidates": len(hypotheses)}

    winner.payload.setdefault("meta", {})["consensus"] = consensus_info

    ensure_dir(out_path.parent)
    dump_json(out_path, winner.payload)

    status = "ok"
    reasons: list[str] = []
    if winner.recognition_confidence < 0.18:
        status = "needs_review"
        reasons.append(f"low number recognition confidence ({winner.recognition_confidence:.3f})")
    if not winner.parse_ok:
        status = "needs_review"
        reasons.append("failed zip parser constraints")
    if winner.n <= 8 and not winner.solver_ok:
        status = "needs_review"
        reasons.append("failed zip solver constraints")

    reasons.append(f"consensus_mode={consensus_info.get('mode')}")
    reasons.append(f"hypotheses={consensus_info.get('candidates')}")
    if "signature_agreement" in consensus_info:
        reasons.append(f"signature_agreement={consensus_info['signature_agreement']}")
    if "unique_signatures" in consensus_info:
        reasons.append(f"unique_signatures={consensus_info['unique_signatures']}")

    return {
        "video_basename": entry.get("video_basename"),
        "playlist_index": entry.get("playlist_index"),
        "video_id": entry.get("video_id"),
        "puzzle_number": entry.get("puzzle_number"),
        "puzzle_date": entry.get("puzzle_date"),
        "grid_image": relative_to_cwd(winner.frame_path),
        "json_path": relative_to_cwd(out_path),
        "n": int(winner.n),
        "checkpoint_count": len(winner.numbers),
        "recognition_confidence": round(float(winner.recognition_confidence), 5),
        "status": status,
        "notes": reasons,
    }


def main() -> int:
    args = parse_args()

    index_path = Path(args.index)
    out_dir = Path(args.out_dir)
    manifest_path = Path(args.manifest)

    ensure_dir(out_dir)
    ensure_dir(manifest_path.parent)

    index_payload = load_json(index_path, default={})
    entries = list(index_payload.get("entries", []))
    if args.only_video:
        entries = [e for e in entries if isinstance(e, dict) and e.get("video_basename") == args.only_video]
    if args.limit is not None:
        entries = entries[: args.limit]

    if not entries:
        print(f"No entries in {index_path}")
        return 0

    knn = build_digit_knn()

    results: list[dict] = []
    for idx, entry in enumerate(entries, start=1):
        result = convert_one(entry, out_dir=out_dir, knn=knn, args=args)
        results.append(result)

        if args.verbose:
            print(
                f"[{idx}/{len(entries)}] {entry.get('video_basename')} -> "
                f"{result.get('status')} ({result.get('json_path', 'no output')})"
            )

    ok_count = sum(1 for item in results if item.get("status") == "ok")
    review_count = len(results) - ok_count

    payload = {
        "generated_at": utc_now_iso(),
        "source_index": str(index_path),
        "count": len(results),
        "ok": ok_count,
        "needs_review": review_count,
        "entries": sorted(
            results,
            key=lambda item: (
                item.get("playlist_index") is None,
                item.get("playlist_index") or 10**9,
                item.get("video_basename", ""),
            ),
        ),
    }

    dump_json(manifest_path, payload)
    print(f"Wrote puzzles manifest: {manifest_path} (ok={ok_count}, needs_review={review_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
