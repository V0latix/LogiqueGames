# Rapport Brownfield — LinkedIn Games Solver
> Généré le 2026-03-26 via /workflows/bmad-brownfield

## État des artifacts BMAD

| Artifact | Statut | Action effectuée |
|----------|--------|-----------------|
| `project-context.md` | ✅ Mis à jour | Corrigé : "0 tests" → 27 fichiers, statut réel |
| `architecture.md` | ✅ À jour | Aucune modification nécessaire |
| `prd.md` | ✅ Mis à jour | Corrigé : statut tests backend |
| `CLAUDE.md` | ✅ Créé | Nouveau fichier de règles essentielles |
| `epic-1-tests-fixtures.md` | ✅ Créé | In Progress — priorité haute |
| `epic-2-frontend-features.md` | ✅ Créé | Backlog |
| `epic-3-dataset-growth.md` | ✅ Créé | Backlog |
| Stories (9 fichiers) | ✅ Créées | `docs/stories/` |

## État du codebase

- Fichiers Python : 85
- Fichiers de test : 27 (1223 lignes)
- Tests passants : **36 / 59**
- Tests en échec : **23 / 59** (fixtures manquantes)
- Dernière activité : 2026-03-26
- Frontend : App.tsx 1249 lignes, 3 puzzles par jeu

## Problème critique identifié

**23 tests échouent** car `data/curated/queens/` et `data/curated/zip/` sont vides.
Les tests référencent `example_6x6.json` et `zip_n4_01.json` qui n'existent pas.

→ Prochaine étape immédiate : **Story 1.1 + Story 1.2**

## Observations

### Points forts
- Architecture modulaire exemplaire (un dossier par jeu, pattern uniforme)
- 7 algorithmes Queens + 5 algorithmes Zip — base de comparaison solide
- Pipeline d'extraction vidéo reproductible (scripts 00→07 idempotents)
- Frontend SPA fonctionnel avec dark mode + mobile responsive

### Risques identifiés
- `App.tsx` monolithique (1249 lignes) — debt de découpage
- 0 intégration CI/CD — tests jamais automatisés
- Fixtures de test absentes → 39% des tests en échec
- README parle uniquement du pipeline Zip (ne reflète pas l'étendue du projet)

### Pièges à éviter
- Ne pas modifier `web/public/data/*.json` directement — passer par le pipeline
- Ne pas découper App.tsx sans plan approuvé
- Ne pas ajouter de dépendances backend (le site est statique)
- `data/curated/` contient les fixtures de test — ne pas gitignorer

## Backlog priorisé

| Priorité | Story | Effort | Valeur |
|----------|-------|--------|--------|
| 🔴 Haute | 1.1 — Fixtures Queens | S | Débloque 12 tests |
| 🔴 Haute | 1.2 — Fixtures Zip | S | Débloque 11 tests |
| 🟡 Haute | 1.3 — Coverage solvers | M | Qualité code |
| 🟡 Moyenne | 2.1 — Bouton Solve | M | UX joueur |
| 🟡 Moyenne | 2.2 — Sélection puzzle | S | UX joueur |
| 🟢 Basse | 3.1 — Pipeline 50+ Zip | L | Dataset |
| 🟢 Basse | 3.3 — Génération Queens | M | Dataset |
| 🟢 Basse | 2.3 — Historique | M | UX joueur |
| 🟢 Basse | 3.2 — Classification | S | Dataset |

## Recommandations

```
Pour corriger les tests immédiatement → /workflows/feature-dev story-1.1-queens-fixtures
Pour ajouter le bouton Solve          → /workflows/feature-dev story-2.1-solve-button
Pour un small fix                     → /workflows/bmad-quick [description]
```
