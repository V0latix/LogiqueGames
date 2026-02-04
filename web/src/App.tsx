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
        <section className="panel">
          <div className="view-header">
            <h1>Tableau de bord</h1>
            <p>Un aperçu rapide de la progression et des actions disponibles.</p>
          </div>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Puzzles terminés</div>
              <div className="stat-value">12</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Temps moyen</div>
              <div className="stat-value">04:32</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Série actuelle</div>
              <div className="stat-value">5 jours</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Niveau</div>
              <div className="stat-value">Intermédiaire</div>
            </div>
          </div>
        </section>

        <div style={{ height: 20 }} />

        <section className="card-grid">
          <div className="card">
            <div className="card-title">Démarrer un puzzle</div>
            <div className="card-text">
              Lance immédiatement une nouvelle grille avec les dernières règles configurées.
            </div>
            <button className="cta" type="button">
              Continuer
            </button>
          </div>
          <div className="card">
            <div className="card-title">Statistiques avancées</div>
            <div className="card-text">
              Analyse tes performances et identifie les patterns de résolution.
            </div>
            <button className="secondary" type="button">
              Voir le détail
            </button>
          </div>
          <div className="card">
            <div className="card-title">Mode focus</div>
            <div className="card-text">
              Une interface épurée pour résoudre sans distraction.
            </div>
            <button className="secondary" type="button">
              Activer
            </button>
          </div>
        </section>

        <div style={{ height: 28 }} />

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
