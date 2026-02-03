const tabs = Array.from(document.querySelectorAll('.tab'));
const views = {
  queens: document.getElementById('view-queens'),
  zip: document.getElementById('view-zip'),
};

function setActiveView(viewName) {
  Object.values(views).forEach((view) => view.classList.remove('active'));
  tabs.forEach((tab) => tab.classList.remove('active'));

  const view = views[viewName] ?? views.queens;
  view.classList.add('active');

  const activeTab = tabs.find((tab) => tab.dataset.view === viewName) ?? tabs[0];
  activeTab.classList.add('active');

  if (window.location.hash !== `#${viewName}`) {
    window.history.replaceState({}, '', `#${viewName}`);
  }
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    setActiveView(tab.dataset.view);
  });
});

const initialView = window.location.hash.replace('#', '') || 'queens';
setActiveView(initialView);

const queensBoard = document.getElementById('queens-board');
const queensStatus = document.getElementById('queens-status');
const queensReset = document.getElementById('queens-reset');
const queensVerify = document.getElementById('queens-verify');
const queensHint = document.getElementById('queens-hint');
const queensNext = document.getElementById('queens-next');

const zipBoard = document.getElementById('zip-board');
const zipStatus = document.getElementById('zip-status');
const zipReset = document.getElementById('zip-reset');
const zipVerify = document.getElementById('zip-verify');
const zipNext = document.getElementById('zip-next');
const zipHint = document.getElementById('zip-hint');

const queensState = {
  puzzles: [],
  current: null,
  currentIndex: null,
  queens: new Set(),
  marks: new Set(),
  cellElements: [],
  solved: false,
};

const zipState = {
  puzzles: [],
  current: null,
  currentIndex: null,
  path: [],
  cellElements: [],
  numberElements: new Map(),
  numberByKey: new Map(),
  solved: false,
};

const dragState = {
  active: false,
  moved: false,
  startKey: null,
  lastKey: null,
  markingStarted: false,
};

const zipDragState = {
  active: false,
  lastKey: null,
};

function cellKey(r, c) {
  return `${r},${c}`;
}

function parseCellKey(key) {
  const [r, c] = key.split(',').map(Number);
  return [r, c];
}

function setQueensStatus(message, type = null) {
  queensStatus.textContent = message;
  queensStatus.classList.remove('ok', 'error', 'warn');
  if (type) {
    queensStatus.classList.add(type);
  }
}

function setZipStatus(message, type = null) {
  zipStatus.textContent = message;
  zipStatus.classList.remove('ok', 'error', 'warn');
  if (type) {
    zipStatus.classList.add(type);
  }
}

function normalizeQueensPuzzle(raw) {
  const regionIds = new Set();
  raw.regions.forEach((row) => row.forEach((id) => regionIds.add(id)));

  const givensQueens = new Set(
    (raw.givens?.queens ?? []).map(([r, c]) => cellKey(r, c))
  );
  const blocked = new Set(
    (raw.givens?.blocked ?? []).map(([r, c]) => cellKey(r, c))
  );

  const palette = [
    '#e7f27c',
    '#ff8a73',
    '#b9e6a5',
    '#e6e3e0',
    '#9fc4ff',
    '#c7b0ea',
    '#ffd2a1',
    '#f3b7d4',
    '#b8f1ed',
    '#d9f7a1',
  ];
  const ids = Array.from(regionIds).sort((a, b) => a - b);
  const regionColors = new Map();
  ids.forEach((id, index) => {
    regionColors.set(id, {
      bg: palette[index % palette.length],
    });
  });

  return {
    ...raw,
    regionIds,
    regionColors,
    givensQueens,
    blocked,
    solutionCols: null,
  };
}

function normalizeWallKey(aKey, bKey) {
  return aKey < bKey ? `${aKey}|${bKey}` : `${bKey}|${aKey}`;
}

function normalizeZipPuzzle(raw) {
  const numberByKey = new Map();
  const numberToKey = new Map();
  raw.numbers.forEach(({ k, r, c }) => {
    const key = cellKey(r, c);
    numberByKey.set(key, k);
    numberToKey.set(k, key);
  });

  const walls = new Set();
  raw.walls.forEach(({ r1, c1, r2, c2 }) => {
    const aKey = cellKey(r1, c1);
    const bKey = cellKey(r2, c2);
    walls.add(normalizeWallKey(aKey, bKey));
  });

  const neighbors = new Map();
  for (let r = 0; r < raw.n; r += 1) {
    for (let c = 0; c < raw.n; c += 1) {
      const key = cellKey(r, c);
      const list = [];
      const candidates = [
        [r - 1, c],
        [r + 1, c],
        [r, c - 1],
        [r, c + 1],
      ];
      candidates.forEach(([nr, nc]) => {
        if (nr < 0 || nc < 0 || nr >= raw.n || nc >= raw.n) {
          return;
        }
        const neighborKey = cellKey(nr, nc);
        if (!walls.has(normalizeWallKey(key, neighborKey))) {
          list.push(neighborKey);
        }
      });
      neighbors.set(key, list);
    }
  }

  return {
    ...raw,
    numberByKey,
    numberToKey,
    walls,
    neighbors,
  };
}

function renderQueensBoard(puzzle) {
  const n = puzzle.n;
  queensBoard.innerHTML = '';
  queensBoard.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
  queensBoard.style.gridTemplateRows = `repeat(${n}, 1fr)`;

  queensState.cellElements = [];

  for (let r = 0; r < n; r += 1) {
    const row = [];
    for (let c = 0; c < n; c += 1) {
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'cell';
      cell.dataset.r = String(r);
      cell.dataset.c = String(c);

      const regionId = puzzle.regions[r][c];
      const colors = puzzle.regionColors.get(regionId);
      if (colors) {
        cell.style.setProperty('--region-bg', colors.bg);
      }

      const key = cellKey(r, c);
      if (puzzle.blocked.has(key)) {
        cell.classList.add('blocked');
        cell.textContent = '×';
        cell.disabled = true;
      } else if (puzzle.givensQueens.has(key)) {
        cell.classList.add('given', 'queen');
        cell.textContent = '♛';
        cell.disabled = true;
      }

      queensBoard.appendChild(cell);
      row.push(cell);
    }
    queensState.cellElements.push(row);
  }
}

function renderZipBoard(puzzle) {
  const n = puzzle.n;
  zipBoard.innerHTML = '';
  zipBoard.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
  zipBoard.style.gridTemplateRows = `repeat(${n}, 1fr)`;

  zipState.cellElements = [];
  zipState.numberElements = new Map();
  zipState.numberByKey = puzzle.numberByKey;

  for (let r = 0; r < n; r += 1) {
    const row = [];
    for (let c = 0; c < n; c += 1) {
      const cell = document.createElement('div');
      cell.className = 'zip-cell';
      cell.dataset.r = String(r);
      cell.dataset.c = String(c);

      const key = cellKey(r, c);
      const number = puzzle.numberByKey.get(key);
      if (number !== undefined) {
        cell.classList.add('has-number');
        const badge = document.createElement('div');
        badge.className = 'zip-number';
        badge.textContent = String(number);
        cell.appendChild(badge);
        zipState.numberElements.set(key, badge);
      }

      const north = r > 0 ? cellKey(r - 1, c) : null;
      const south = r < n - 1 ? cellKey(r + 1, c) : null;
      const west = c > 0 ? cellKey(r, c - 1) : null;
      const east = c < n - 1 ? cellKey(r, c + 1) : null;

      if (north && puzzle.walls.has(normalizeWallKey(key, north))) {
        cell.classList.add('wall-top');
      }
      if (south && puzzle.walls.has(normalizeWallKey(key, south))) {
        cell.classList.add('wall-bottom');
      }
      if (west && puzzle.walls.has(normalizeWallKey(key, west))) {
        cell.classList.add('wall-left');
      }
      if (east && puzzle.walls.has(normalizeWallKey(key, east))) {
        cell.classList.add('wall-right');
      }

      zipBoard.appendChild(cell);
      row.push(cell);
    }
    zipState.cellElements.push(row);
  }
}

function computeQueensConflicts(puzzle, queensSet) {
  const n = puzzle.n;
  const positions = [];
  queensSet.forEach((key) => {
    const [r, c] = parseCellKey(key);
    positions.push({ r, c, key });
  });

  const rowCounts = Array.from({ length: n }, () => 0);
  const colCounts = Array.from({ length: n }, () => 0);
  const regionCounts = new Map();

  positions.forEach(({ r, c }) => {
    rowCounts[r] += 1;
    colCounts[c] += 1;
    const regionId = puzzle.regions[r][c];
    regionCounts.set(regionId, (regionCounts.get(regionId) ?? 0) + 1);
  });

  const conflicts = new Set();

  positions.forEach(({ r, c, key }) => {
    const regionId = puzzle.regions[r][c];
    if (rowCounts[r] > 1 || colCounts[c] > 1 || (regionCounts.get(regionId) ?? 0) > 1) {
      conflicts.add(key);
    }
  });

  const queenKeys = new Set(positions.map((pos) => pos.key));
  positions.forEach(({ r, c, key }) => {
    for (let dr = -1; dr <= 1; dr += 1) {
      for (let dc = -1; dc <= 1; dc += 1) {
        if (dr === 0 && dc === 0) {
          continue;
        }
        const nr = r + dr;
        const nc = c + dc;
        if (nr < 0 || nc < 0 || nr >= n || nc >= n) {
          continue;
        }
        const neighborKey = cellKey(nr, nc);
        if (queenKeys.has(neighborKey)) {
          conflicts.add(key);
          conflicts.add(neighborKey);
        }
      }
    }
  });

  positions.forEach(({ key }) => {
    if (puzzle.blocked.has(key)) {
      conflicts.add(key);
    }
  });

  return conflicts;
}

function updateQueensStatusInfo() {
  const puzzle = queensState.current;
  if (!puzzle) {
    return;
  }
  const total = puzzle.n;
  const placed = queensState.queens.size;
  const conflicts = computeQueensConflicts(puzzle, queensState.queens);
  const solved =
    placed === total &&
    conflicts.size === 0 &&
    validateQueensSolution(puzzle, queensState.queens).ok;

  queensState.solved = solved;

  if (solved) {
    setQueensStatus("C'est bien, t'as reussi. Clique sur \"Puzzle suivant\".", 'ok');
    return;
  }

  let message = `Puzzle ${puzzle.id} · ${puzzle.n}x${puzzle.n}. Reines: ${placed}/${total}.`;
  let type = null;
  if (conflicts.size > 0) {
    message += ` Conflits: ${conflicts.size}.`;
    type = 'warn';
  } else if (placed === total) {
    message += ' Aucune erreur visible.';
  }
  setQueensStatus(message, type);
}

function updateZipStatusInfo() {
  const puzzle = zipState.current;
  if (!puzzle) {
    return;
  }
  const total = puzzle.n * puzzle.n;
  const placed = zipState.path.length;
  const solved = placed === total && validateZipSolution(puzzle, zipState.path).ok;
  zipState.solved = solved;

  if (solved) {
    setZipStatus("C'est bien, t'as reussi. Clique sur \"Puzzle suivant\".", 'ok');
    return;
  }

  let message = `Puzzle ${puzzle.id} · ${puzzle.n}x${puzzle.n}. Parcours: ${placed}/${total}.`;
  setZipStatus(message, null);
}

function updateQueensUI() {
  const puzzle = queensState.current;
  if (!puzzle) {
    return;
  }

  const conflicts = computeQueensConflicts(puzzle, queensState.queens);

  for (let r = 0; r < puzzle.n; r += 1) {
    for (let c = 0; c < puzzle.n; c += 1) {
      const cell = queensState.cellElements[r][c];
      const key = cellKey(r, c);
      const isGiven = puzzle.givensQueens.has(key);
      const isBlocked = puzzle.blocked.has(key);
      const isQueen = queensState.queens.has(key) || isGiven;
      const isMark = queensState.marks.has(key);

      if (!isBlocked && !isGiven) {
        if (isQueen) {
          cell.textContent = '♛';
        } else if (isMark) {
          cell.textContent = '×';
        } else {
          cell.textContent = '';
        }
      }

      cell.classList.toggle('queen', isQueen);
      cell.classList.toggle('mark', !isQueen && isMark);
      cell.classList.toggle('conflict', isQueen && conflicts.has(key));
    }
  }

  updateQueensStatusInfo();
}

function directionFromTo(fromKey, toKey) {
  const [fr, fc] = parseCellKey(fromKey);
  const [tr, tc] = parseCellKey(toKey);
  if (tr === fr - 1 && tc === fc) {
    return 'n';
  }
  if (tr === fr + 1 && tc === fc) {
    return 's';
  }
  if (tr === fr && tc === fc - 1) {
    return 'w';
  }
  if (tr === fr && tc === fc + 1) {
    return 'e';
  }
  return null;
}

function applyZipPathStyles(cell, segments) {
  if (!segments || segments.size === 0) {
    cell.style.backgroundImage = '';
    cell.style.backgroundSize = '';
    cell.style.backgroundPosition = '';
    cell.style.backgroundRepeat = '';
    return;
  }

  const color = 'var(--zip-path)';
  const gradients = [];
  const sizes = [];
  const positions = [];
  const stroke = 'var(--zip-stroke)';
  const node = 'var(--zip-node)';

  if (segments.has('n')) {
    gradients.push(`linear-gradient(${color}, ${color})`);
    sizes.push(`${stroke} 50%`);
    positions.push('center top');
  }
  if (segments.has('s')) {
    gradients.push(`linear-gradient(${color}, ${color})`);
    sizes.push(`${stroke} 50%`);
    positions.push('center bottom');
  }
  if (segments.has('w')) {
    gradients.push(`linear-gradient(${color}, ${color})`);
    sizes.push(`50% ${stroke}`);
    positions.push('left center');
  }
  if (segments.has('e')) {
    gradients.push(`linear-gradient(${color}, ${color})`);
    sizes.push(`50% ${stroke}`);
    positions.push('right center');
  }

  if (segments.has('n') && !segments.has('s')) {
    gradients.push(`radial-gradient(circle, ${color} 0 60%, transparent 61%)`);
    sizes.push(`${stroke} ${stroke}`);
    positions.push('center top');
  }
  if (segments.has('s') && !segments.has('n')) {
    gradients.push(`radial-gradient(circle, ${color} 0 60%, transparent 61%)`);
    sizes.push(`${stroke} ${stroke}`);
    positions.push('center bottom');
  }
  if (segments.has('w') && !segments.has('e')) {
    gradients.push(`radial-gradient(circle, ${color} 0 60%, transparent 61%)`);
    sizes.push(`${stroke} ${stroke}`);
    positions.push('left center');
  }
  if (segments.has('e') && !segments.has('w')) {
    gradients.push(`radial-gradient(circle, ${color} 0 60%, transparent 61%)`);
    sizes.push(`${stroke} ${stroke}`);
    positions.push('right center');
  }

  gradients.push(`radial-gradient(circle, ${color} 0 60%, transparent 61%)`);
  sizes.push(`${node} ${node}`);
  positions.push('center center');

  cell.style.backgroundImage = gradients.join(', ');
  cell.style.backgroundSize = sizes.join(', ');
  cell.style.backgroundPosition = positions.join(', ');
  cell.style.backgroundRepeat = 'no-repeat';
}

function updateZipUI() {
  const puzzle = zipState.current;
  if (!puzzle) {
    return;
  }

  const path = zipState.path;
  const pathSet = new Set(path);
  const lastKey = path.length ? path[path.length - 1] : null;
  const indexByKey = new Map();
  path.forEach((key, index) => {
    indexByKey.set(key, index);
  });

  for (let r = 0; r < puzzle.n; r += 1) {
    for (let c = 0; c < puzzle.n; c += 1) {
      const cell = zipState.cellElements[r][c];
      const key = cellKey(r, c);
      const isPath = pathSet.has(key);
      const isActive = lastKey === key;
      cell.classList.toggle('path', isPath);
      cell.classList.toggle('active', isActive);

      const numberElement = zipState.numberElements.get(key);
      if (numberElement) {
        numberElement.classList.toggle('active', isActive);
      }

      if (!isPath) {
        applyZipPathStyles(cell, null);
        continue;
      }

      const segments = new Set();
      const index = indexByKey.get(key);
      if (index > 0) {
        const prevKey = path[index - 1];
        const dir = directionFromTo(key, prevKey);
        if (dir) {
          segments.add(dir);
        }
      }
      if (index < path.length - 1) {
        const nextKey = path[index + 1];
        const dir = directionFromTo(key, nextKey);
        if (dir) {
          segments.add(dir);
        }
      }

      applyZipPathStyles(cell, segments);
    }
  }

  updateZipStatusInfo();
}

function validateZipPrefix(puzzle, path) {
  const seen = new Set();
  let lastKey = null;
  let maxNumberSeen = 0;

  for (const key of path) {
    if (seen.has(key)) {
      return { ok: false, reason: 'Une case est visitee plusieurs fois.', maxNumberSeen };
    }
    seen.add(key);

    if (lastKey) {
      const neighbors = puzzle.neighbors.get(lastKey) ?? [];
      if (!neighbors.includes(key)) {
        return {
          ok: false,
          reason: 'Le chemin doit rester adjacent et respecter les murs.',
          maxNumberSeen,
        };
      }
    }

    const number = puzzle.numberByKey.get(key);
    if (number !== undefined) {
      if (number !== maxNumberSeen + 1) {
        return { ok: false, reason: "Les nombres doivent etre visites dans l'ordre.", maxNumberSeen };
      }
      maxNumberSeen = number;
    }

    lastKey = key;
  }

  return { ok: true, reason: null, maxNumberSeen };
}

function orderZipNeighbors(neighbors, puzzle, visited, maxNumberSeen) {
  const nextNumber = maxNumberSeen + 1;
  return neighbors
    .filter((key) => !visited.has(key))
    .map((key) => {
      const number = puzzle.numberByKey.get(key);
      const priority = number === nextNumber ? -100 : 0;
      const degree = (puzzle.neighbors.get(key) ?? []).filter((n) => !visited.has(n)).length;
      return { key, score: priority + degree };
    })
    .sort((a, b) => a.score - b.score)
    .map((entry) => entry.key);
}

function solveZip(puzzle, prefixPath) {
  const total = puzzle.n * puzzle.n;
  let path = [...prefixPath];
  let visited = new Set(path);

  if (path.length === 0) {
    const startKey = puzzle.numberToKey.get(1);
    if (!startKey) {
      return null;
    }
    path = [startKey];
    visited = new Set(path);
  }

  const validation = validateZipPrefix(puzzle, path);
  if (!validation.ok) {
    return null;
  }

  function dfs(currentPath, currentVisited, maxNumberSeen) {
    if (currentPath.length === total) {
      return [...currentPath];
    }

    const currentKey = currentPath[currentPath.length - 1];
    const neighbors = puzzle.neighbors.get(currentKey) ?? [];
    const ordered = orderZipNeighbors(neighbors, puzzle, currentVisited, maxNumberSeen);

    for (const nextKey of ordered) {
      const number = puzzle.numberByKey.get(nextKey);
      if (number !== undefined && number !== maxNumberSeen + 1) {
        continue;
      }
      const nextMax = number ?? maxNumberSeen;

      currentVisited.add(nextKey);
      currentPath.push(nextKey);

      const result = dfs(currentPath, currentVisited, nextMax);
      if (result) {
        return result;
      }

      currentPath.pop();
      currentVisited.delete(nextKey);
    }

    return null;
  }

  return dfs(path, visited, validation.maxNumberSeen);
}

function validateQueensSolution(puzzle, queensSet) {
  const n = puzzle.n;
  const positions = [];
  queensSet.forEach((key) => {
    const [r, c] = parseCellKey(key);
    positions.push({ r, c, key });
  });

  for (const key of puzzle.givensQueens) {
    if (!queensSet.has(key)) {
      return { ok: false, reason: 'Les reines donnees doivent rester en place.' };
    }
  }

  for (const { key } of positions) {
    if (puzzle.blocked.has(key)) {
      return { ok: false, reason: 'Une reine est placee sur une case interdite.' };
    }
  }

  if (positions.length !== n) {
    return { ok: false, reason: `Il faut exactement ${n} reines.` };
  }

  const rowCounts = Array.from({ length: n }, () => 0);
  const colCounts = Array.from({ length: n }, () => 0);
  const regionCounts = new Map();

  positions.forEach(({ r, c }) => {
    rowCounts[r] += 1;
    colCounts[c] += 1;
    const regionId = puzzle.regions[r][c];
    regionCounts.set(regionId, (regionCounts.get(regionId) ?? 0) + 1);
  });

  if (rowCounts.some((count) => count !== 1)) {
    return { ok: false, reason: 'Chaque ligne doit contenir exactement une reine.' };
  }

  if (colCounts.some((count) => count !== 1)) {
    return { ok: false, reason: 'Chaque colonne doit contenir exactement une reine.' };
  }

  for (const id of puzzle.regionIds) {
    if ((regionCounts.get(id) ?? 0) !== 1) {
      return { ok: false, reason: 'Chaque region doit contenir exactement une reine.' };
    }
  }

  const queenKeys = new Set(positions.map((pos) => pos.key));
  for (const { r, c } of positions) {
    for (let dr = -1; dr <= 1; dr += 1) {
      for (let dc = -1; dc <= 1; dc += 1) {
        if (dr === 0 && dc === 0) {
          continue;
        }
        const nr = r + dr;
        const nc = c + dc;
        if (nr < 0 || nc < 0 || nr >= n || nc >= n) {
          continue;
        }
        if (queenKeys.has(cellKey(nr, nc))) {
          return { ok: false, reason: 'Les reines ne peuvent pas etre adjacentes.' };
        }
      }
    }
  }

  return { ok: true, reason: null };
}

function validateZipSolution(puzzle, path) {
  const n = puzzle.n;
  if (path.length !== n * n) {
    return { ok: false, reason: 'Le chemin doit couvrir toute la grille.' };
  }

  const seen = new Set();
  for (let i = 0; i < path.length; i += 1) {
    const key = path[i];
    if (seen.has(key)) {
      return { ok: false, reason: 'Une case est visitee plusieurs fois.' };
    }
    seen.add(key);

    if (i > 0) {
      const prev = path[i - 1];
      const neighbors = puzzle.neighbors.get(prev) ?? [];
      if (!neighbors.includes(key)) {
        return { ok: false, reason: 'Le chemin doit rester adjacent et respecter les murs.' };
      }
    }
  }

  const positions = new Map();
  path.forEach((key, index) => {
    positions.set(key, index);
  });

  const numbers = Array.from(puzzle.numberToKey.keys());
  const maxNumber = numbers.length ? Math.max(...numbers) : 0;

  let lastIndex = -1;
  for (let k = 1; k <= maxNumber; k += 1) {
    const key = puzzle.numberToKey.get(k);
    if (!key) {
      return { ok: false, reason: `Nombre ${k} manquant.` };
    }
    const idx = positions.get(key);
    if (idx === undefined) {
      return { ok: false, reason: `Le nombre ${k} n'est pas visite.` };
    }
    if (idx <= lastIndex) {
      return { ok: false, reason: 'Les nombres doivent etre visites dans l\'ordre.' };
    }
    lastIndex = idx;
  }

  return { ok: true, reason: null };
}

function solveQueens(puzzle) {
  if (puzzle.solutionCols) {
    return puzzle.solutionCols;
  }

  const n = puzzle.n;
  const fixedCols = Array(n).fill(-1);

  for (const key of puzzle.givensQueens) {
    const [r, c] = parseCellKey(key);
    if (fixedCols[r] !== -1 && fixedCols[r] !== c) {
      return null;
    }
    fixedCols[r] = c;
  }

  const usedCols = new Set();
  const usedRegions = new Set();
  const cols = Array(n).fill(-1);

  function backtrack(row, prevCol) {
    if (row === n) {
      return true;
    }

    const fixed = fixedCols[row];
    const candidates = fixed >= 0 ? [fixed] : Array.from({ length: n }, (_, i) => i);

    for (const col of candidates) {
      const key = cellKey(row, col);
      if (puzzle.blocked.has(key)) {
        continue;
      }
      if (usedCols.has(col)) {
        continue;
      }
      const regionId = puzzle.regions[row][col];
      if (usedRegions.has(regionId)) {
        continue;
      }
      if (prevCol !== null && Math.abs(col - prevCol) <= 1) {
        continue;
      }

      usedCols.add(col);
      usedRegions.add(regionId);
      cols[row] = col;

      if (backtrack(row + 1, col)) {
        return true;
      }

      usedCols.delete(col);
      usedRegions.delete(regionId);
      cols[row] = -1;
    }

    return false;
  }

  if (!backtrack(0, null)) {
    return null;
  }

  puzzle.solutionCols = cols;
  return cols;
}

function applyQueensHint() {
  const puzzle = queensState.current;
  if (!puzzle) {
    return;
  }

  const solution = solveQueens(puzzle);
  if (!solution) {
    setQueensStatus('Indice indisponible pour ce puzzle.', 'error');
    return;
  }

  const solutionKeys = solution.map((col, row) => cellKey(row, col));
  for (const key of solutionKeys) {
    if (!queensState.queens.has(key)) {
      queensState.queens.add(key);
      queensState.marks.delete(key);
      updateQueensUI();
      setQueensStatus('Indice applique: une reine a ete ajoutee.', 'ok');
      return;
    }
  }

  setQueensStatus('Toutes les reines sont deja placees.', 'ok');
}

function applyZipHint() {
  const puzzle = zipState.current;
  if (!puzzle) {
    return;
  }

  const prefix = [...zipState.path];
  const validation = validateZipPrefix(puzzle, prefix);
  if (!validation.ok) {
    setZipStatus(validation.reason ?? 'Chemin invalide.', 'error');
    return;
  }

  if (prefix.length === 0) {
    const startKey = puzzle.numberToKey.get(1);
    if (startKey) {
      zipState.path = [startKey];
      updateZipUI();
      setZipStatus('Indice applique : depart place.', 'ok');
      return;
    }
  }

  const solution = solveZip(puzzle, prefix);
  if (!solution) {
    setZipStatus('Indice indisponible pour ce chemin.', 'error');
    return;
  }

  if (solution.length <= prefix.length) {
    setZipStatus('Toutes les cases sont deja remplies.', 'ok');
    return;
  }

  const nextKey = solution[prefix.length];
  zipState.path = [...prefix, nextKey];
  updateZipUI();
  setZipStatus('Indice applique : etape suivante ajoutee.', 'ok');
}

function setQueensPuzzle(puzzle) {
  queensState.current = puzzle;
  queensState.queens = new Set(puzzle.givensQueens);
  queensState.marks = new Set();
  queensState.solved = false;
  renderQueensBoard(puzzle);
  updateQueensUI();
}

function setZipPuzzle(puzzle) {
  zipState.current = puzzle;
  zipState.path = [];
  zipState.solved = false;
  renderZipBoard(puzzle);
  updateZipUI();
}

function pickRandomPuzzleIndex(excludeIndex, puzzles) {
  const count = puzzles.length;
  if (count === 0) {
    return null;
  }
  if (count === 1) {
    return 0;
  }
  let index = Math.floor(Math.random() * count);
  while (index === excludeIndex) {
    index = Math.floor(Math.random() * count);
  }
  return index;
}

function pickNextPuzzle(state) {
  const nextIndex = pickRandomPuzzleIndex(state.currentIndex, state.puzzles);
  if (nextIndex === null) {
    return null;
  }
  state.currentIndex = nextIndex;
  return state.puzzles[nextIndex];
}

function isInteractiveCell(key, puzzle) {
  return !puzzle.blocked.has(key) && !puzzle.givensQueens.has(key);
}

function markCell(key, puzzle) {
  if (!isInteractiveCell(key, puzzle)) {
    return false;
  }
  if (queensState.queens.has(key)) {
    return false;
  }
  queensState.marks.add(key);
  return true;
}

function cycleCellState(key, puzzle) {
  if (!isInteractiveCell(key, puzzle)) {
    return;
  }

  if (queensState.queens.has(key)) {
    queensState.queens.delete(key);
  } else if (queensState.marks.has(key)) {
    queensState.marks.delete(key);
    queensState.queens.add(key);
  } else {
    queensState.marks.add(key);
  }
}

function getCellFromEvent(event) {
  const element = document.elementFromPoint(event.clientX, event.clientY);
  return element ? element.closest('.cell') : null;
}

function getZipCellFromEvent(event) {
  const element = document.elementFromPoint(event.clientX, event.clientY);
  return element ? element.closest('.zip-cell') : null;
}

function resetDragState() {
  dragState.active = false;
  dragState.moved = false;
  dragState.startKey = null;
  dragState.lastKey = null;
  dragState.markingStarted = false;
}

function resetZipDragState() {
  zipDragState.active = false;
  zipDragState.lastKey = null;
}

queensBoard.addEventListener('pointerdown', (event) => {
  const target = event.target.closest('.cell');
  if (!target || !queensState.current) {
    return;
  }
  const r = Number(target.dataset.r);
  const c = Number(target.dataset.c);
  const key = cellKey(r, c);
  const puzzle = queensState.current;

  if (!isInteractiveCell(key, puzzle)) {
    return;
  }

  event.preventDefault();
  dragState.active = true;
  dragState.moved = false;
  dragState.startKey = key;
  dragState.lastKey = key;
  dragState.markingStarted = false;
  queensBoard.setPointerCapture(event.pointerId);
});

queensBoard.addEventListener('pointermove', (event) => {
  if (!dragState.active || !queensState.current) {
    return;
  }

  const cell = getCellFromEvent(event);
  if (!cell) {
    return;
  }

  const r = Number(cell.dataset.r);
  const c = Number(cell.dataset.c);
  const key = cellKey(r, c);
  if (key === dragState.lastKey) {
    return;
  }

  dragState.moved = true;
  dragState.lastKey = key;

  if (!dragState.markingStarted) {
    markCell(dragState.startKey, queensState.current);
    dragState.markingStarted = true;
  }

  if (markCell(key, queensState.current)) {
    updateQueensUI();
  }
});

function finishPointerInteraction(event) {
  if (!dragState.active || !queensState.current) {
    resetDragState();
    return;
  }

  if (!dragState.moved && dragState.startKey) {
    cycleCellState(dragState.startKey, queensState.current);
    updateQueensUI();
  } else {
    updateQueensUI();
  }

  queensBoard.releasePointerCapture(event.pointerId);
  resetDragState();
}

queensBoard.addEventListener('pointerup', finishPointerInteraction);
queensBoard.addEventListener('pointercancel', finishPointerInteraction);

zipBoard.addEventListener('pointerdown', (event) => {
  const cell = getZipCellFromEvent(event);
  if (!cell || !zipState.current) {
    return;
  }

  event.preventDefault();
  zipDragState.active = true;
  zipDragState.lastKey = null;
  zipBoard.setPointerCapture(event.pointerId);
  handleZipInteraction(cell);
});

zipBoard.addEventListener('pointermove', (event) => {
  if (!zipDragState.active || !zipState.current) {
    return;
  }
  const cell = getZipCellFromEvent(event);
  if (!cell) {
    return;
  }
  handleZipInteraction(cell);
});

function finishZipPointer(event) {
  if (!zipDragState.active) {
    resetZipDragState();
    return;
  }
  zipBoard.releasePointerCapture(event.pointerId);
  resetZipDragState();
}

zipBoard.addEventListener('pointerup', finishZipPointer);
zipBoard.addEventListener('pointercancel', finishZipPointer);

function handleZipInteraction(cell) {
  if (!zipState.current) {
    return;
  }

  const r = Number(cell.dataset.r);
  const c = Number(cell.dataset.c);
  const key = cellKey(r, c);

  if (key === zipDragState.lastKey) {
    return;
  }

  zipDragState.lastKey = key;

  const puzzle = zipState.current;
  const path = zipState.path;
  if (path.length === 0) {
    zipState.path = [key];
    updateZipUI();
    return;
  }

  const lastKey = path[path.length - 1];
  if (key === lastKey) {
    return;
  }

  const existingIndex = path.indexOf(key);
  if (existingIndex !== -1) {
    zipState.path = path.slice(0, existingIndex + 1);
    updateZipUI();
    return;
  }

  const neighbors = puzzle.neighbors.get(lastKey) ?? [];
  if (!neighbors.includes(key)) {
    return;
  }

  zipState.path = [...path, key];
  updateZipUI();
}

queensReset.addEventListener('click', () => {
  if (!queensState.current) {
    return;
  }
  queensState.queens = new Set(queensState.current.givensQueens);
  queensState.marks = new Set();
  updateQueensUI();
});

queensVerify.addEventListener('click', () => {
  if (!queensState.current) {
    return;
  }
  const result = validateQueensSolution(queensState.current, queensState.queens);
  if (result.ok) {
    setQueensStatus('Bravo, solution correcte !', 'ok');
  } else {
    setQueensStatus(result.reason ?? 'Solution incorrecte.', 'error');
  }
});

queensHint.addEventListener('click', () => {
  applyQueensHint();
});

queensNext.addEventListener('click', () => {
  const puzzle = pickNextPuzzle(queensState);
  if (puzzle) {
    setQueensPuzzle(puzzle);
  }
});

zipReset.addEventListener('click', () => {
  if (!zipState.current) {
    return;
  }
  zipState.path = [];
  updateZipUI();
});

zipHint.addEventListener('click', () => {
  applyZipHint();
});

zipVerify.addEventListener('click', () => {
  if (!zipState.current) {
    return;
  }
  const result = validateZipSolution(zipState.current, zipState.path);
  if (result.ok) {
    setZipStatus('Bravo, solution correcte !', 'ok');
  } else {
    setZipStatus(result.reason ?? 'Solution incorrecte.', 'error');
  }
});

zipNext.addEventListener('click', () => {
  const puzzle = pickNextPuzzle(zipState);
  if (puzzle) {
    setZipPuzzle(puzzle);
  }
});

async function loadQueens() {
  setQueensStatus('Chargement des puzzles Queens…');
  try {
    const response = await fetch('./data/queens_unique.json');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    if (data.game !== 'queens' || !Array.isArray(data.puzzles)) {
      throw new Error('Format Queens invalide');
    }

    queensState.puzzles = data.puzzles.map(normalizeQueensPuzzle);
    queensReset.disabled = false;
    queensVerify.disabled = false;
    queensHint.disabled = false;
    queensNext.disabled = false;

    const firstPuzzle = pickNextPuzzle(queensState);
    if (firstPuzzle) {
      setQueensPuzzle(firstPuzzle);
    }
  } catch (error) {
    console.error(error);
    setQueensStatus('Impossible de charger les puzzles Queens.', 'error');
  }
}

async function loadZip() {
  setZipStatus('Chargement des puzzles Zip…');
  try {
    const response = await fetch('./data/zip_unique.json');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    if (data.game !== 'zip' || !Array.isArray(data.puzzles)) {
      throw new Error('Format Zip invalide');
    }

    zipState.puzzles = data.puzzles.map(normalizeZipPuzzle);
    zipReset.disabled = false;
    zipVerify.disabled = false;
    zipNext.disabled = false;
    zipHint.disabled = false;

    const firstPuzzle = pickNextPuzzle(zipState);
    if (firstPuzzle) {
      setZipPuzzle(firstPuzzle);
    }
  } catch (error) {
    console.error(error);
    setZipStatus('Impossible de charger les puzzles Zip.', 'error');
  }
}

loadQueens();
loadZip();
