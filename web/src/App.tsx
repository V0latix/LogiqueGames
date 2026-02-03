import { useState } from 'react';

type View = 'queens' | 'zip';

export default function App() {
  const [view, setView] = useState<View>('queens');

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-dot" />
          <div>
            <div className="brand-title">LinkedIn Games</div>
            <div className="brand-subtitle">Puzzles jouables - Queens &amp; Zip</div>
          </div>
        </div>
        <nav className="tabs">
          <button
            className={`tab ${view === 'queens' ? 'active' : ''}`}
            type="button"
            onClick={() => setView('queens')}
          >
            Queens
          </button>
          <button
            className={`tab ${view === 'zip' ? 'active' : ''}`}
            type="button"
            onClick={() => setView('zip')}
          >
            Zip
          </button>
        </nav>
      </header>

      <main className="page">
        {view === 'queens' ? (
          <section className="view">
            <div className="view-header">
              <h1>Queens</h1>
              <p>Place une reine par ligne, colonne et région, sans contact adjacent.</p>
            </div>
            <div className="layout">
              <section className="board" aria-label="Grille Queens">
                <div className="grid placeholder">Grille Queens (React UI)</div>
              </section>
              <aside className="panel side-panel">
                <div className="panel-actions vertical">
                  <button className="secondary" type="button">
                    Puzzle suivant
                  </button>
                  <button className="secondary" type="button">
                    Réinitialiser
                  </button>
                  <button className="secondary" type="button">
                    Hint
                  </button>
                  <button className="primary" type="button">
                    Vérifier
                  </button>
                </div>
                <div className="panel-status">Chargement…</div>
                <div className="panel-note">
                  Clique sur une case pour placer une croix, puis reclique pour poser une reine.
                </div>
              </aside>
            </div>
          </section>
        ) : (
          <section className="view">
            <div className="view-header">
              <h1>Zip</h1>
              <p>Relie toutes les cases en respectant les murs et les numéros.</p>
            </div>
            <div className="layout">
              <section className="board" aria-label="Grille Zip">
                <div className="zip-grid placeholder">Grille Zip (React UI)</div>
              </section>
              <aside className="panel side-panel">
                <div className="panel-actions vertical">
                  <button className="secondary" type="button">
                    Puzzle suivant
                  </button>
                  <button className="secondary" type="button">
                    Réinitialiser
                  </button>
                  <button className="secondary" type="button">
                    Hint
                  </button>
                  <button className="primary" type="button">
                    Vérifier
                  </button>
                </div>
                <div className="panel-status">Chargement…</div>
                <div className="panel-note">
                  Clique et glisse pour tracer un chemin qui passe par tous les numéros.
                </div>
              </aside>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
