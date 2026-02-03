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

const queensSelect = document.getElementById('queens-select');
const queensBoard = document.getElementById('queens-board');
const queensStatus = document.getElementById('queens-status');
const queensReset = document.getElementById('queens-reset');
const queensVerify = document.getElementById('queens-verify');

const queensState = {
  puzzles: [],
  current: null,
  queens: new Set(),
  cellElements: [],
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

  const ids = Array.from(regionIds).sort((a, b) => a - b);
  const regionColors = new Map();
  ids.forEach((id, index) => {
    const hue = Math.round((index * 360) / ids.length);
    regionColors.set(id, {
      bg: `hsl(${hue} 65% 92%)`,
      border: `hsl(${hue} 55% 72%)`,
    });
  });

  return {
    ...raw,
    regionIds,
    regionColors,
    givensQueens,
    blocked,
  };
}

function buildQueensOptions(puzzles) {
  queensSelect.innerHTML = '';
  puzzles.forEach((puzzle, index) => {
    const option = document.createElement('option');
    const givensCount = puzzle.givensQueens.size;
    const blockedCount = puzzle.blocked.size;
    const givensText = givensCount ? ` · ${givensCount} reine(s)` : '';
    const blockedText = blockedCount ? ` · ${blockedCount} bloquee(s)` : '';
    option.value = String(index);
    option.textContent = `Puzzle ${puzzle.id} · ${puzzle.n}x${puzzle.n}${givensText}${blockedText}`;
    queensSelect.appendChild(option);
  });
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
        cell.style.setProperty('--region-border', colors.border);
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
  let message = `Reines placees: ${placed}/${total}.`;
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

      if (!isBlocked && !isGiven) {
        cell.textContent = isQueen ? '♛' : '';
      }

      cell.classList.toggle('queen', isQueen);
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
  for (const { r, c, key } of positions) {
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

function setQueensPuzzle(puzzle) {
  queensState.current = puzzle;
  queensState.queens = new Set(puzzle.givensQueens);
  renderQueensBoard(puzzle);
  updateQueensUI();
}

queensBoard.addEventListener('click', (event) => {
  const target = event.target.closest('.cell');
  if (!target || !queensState.current) {
    return;
  }
  const r = Number(target.dataset.r);
  const c = Number(target.dataset.c);
  const key = cellKey(r, c);
  const puzzle = queensState.current;

  if (puzzle.blocked.has(key) || puzzle.givensQueens.has(key)) {
    return;
  }

  if (queensState.queens.has(key)) {
    queensState.queens.delete(key);
  } else {
    queensState.queens.add(key);
  }

  updateQueensUI();
});

queensReset.addEventListener('click', () => {
  if (!queensState.current) {
    return;
  }
  queensState.queens = new Set(queensState.current.givensQueens);
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
    buildQueensOptions(queensState.puzzles);
    queensSelect.disabled = false;
    queensReset.disabled = false;
    queensVerify.disabled = false;

    const firstPuzzle = queensState.puzzles[0];
    setQueensPuzzle(firstPuzzle);
    queensSelect.value = '0';
  } catch (error) {
    console.error(error);
    setQueensStatus('Impossible de charger les puzzles Queens.', 'error');
  }
}

queensSelect.addEventListener('change', (event) => {
  const index = Number(event.target.value);
  const puzzle = queensState.puzzles[index];
  if (puzzle) {
    setQueensPuzzle(puzzle);
  }
});

loadQueens();
