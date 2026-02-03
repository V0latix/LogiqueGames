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

const queensState = {
  puzzles: [],
  current: null,
  currentIndex: null,
  queens: new Set(),
  marks: new Set(),
  cellElements: [],
  solved: false,
};

const dragState = {
  active: false,
  moved: false,
  startKey: null,
  lastKey: null,
  markingStarted: false,
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

function setQueensPuzzle(puzzle) {
  queensState.current = puzzle;
  queensState.queens = new Set(puzzle.givensQueens);
  queensState.marks = new Set();
  queensState.solved = false;
  renderQueensBoard(puzzle);
  updateQueensUI();
}

function pickRandomPuzzleIndex(excludeIndex) {
  const count = queensState.puzzles.length;
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

function pickNextPuzzle() {
  const nextIndex = pickRandomPuzzleIndex(queensState.currentIndex);
  if (nextIndex === null) {
    return null;
  }
  queensState.currentIndex = nextIndex;
  return queensState.puzzles[nextIndex];
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

function resetDragState() {
  dragState.active = false;
  dragState.moved = false;
  dragState.startKey = null;
  dragState.lastKey = null;
  dragState.markingStarted = false;
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
  const puzzle = pickNextPuzzle();
  if (puzzle) {
    setQueensPuzzle(puzzle);
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

    const firstPuzzle = pickNextPuzzle();
    if (firstPuzzle) {
      setQueensPuzzle(firstPuzzle);
    }
  } catch (error) {
    console.error(error);
    setQueensStatus('Impossible de charger les puzzles Queens.', 'error');
  }
}

loadQueens();
