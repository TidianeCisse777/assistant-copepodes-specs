# Handoff — IDEA Frontend : design login-match + architecture review

**Date :** 2026-05-28
**Repo principal :** `/Users/tidianecisse/PROJET_INFO/IDEA/frontend/`
**Repo specs :** `/Users/tidianecisse/PROJET_INFO/assistant-copepodes-specs/`

---

## Ce qui a été accompli cette session

### 1. Alignement visuel `index.html` → `login.html` (✅ terminé)

Tous les changements sont dans **`IDEA/frontend/styles.css`** et **`IDEA/frontend/index.html`** — déjà sauvegardés, pas encore commités.

| Modification | Fichier | Détail |
|---|---|---|
| Dot grid background | `styles.css` — `body.theme-dark` | `radial-gradient(rgba(90,172,218,0.04) 1px, transparent 1px)` à 28×28px |
| Font sidebar brand | `styles.css` — `.sidebar-brand-name` | Cormorant Garamond italic, 1rem, fw 400 |
| Accent "Copépodes" | `styles.css` — `.sidebar-brand-name em` | `color: var(--primary)` |
| Modal dark theme | `styles.css` — `body.theme-dark .modal-content` + 9 sélecteurs | Surfaces sombres via CSS vars, plus de `#fefefe`/`white` hardcodés |
| `.session-mode-online` | `styles.css` | Style manquant ajouté (bleu accent `#5aacda`) |
| HTML brand | `index.html` ligne 24 | `IDEA <em>Copépodes</em>` pour activer la règle `em` |

**Référence de design :** `login.html` — tokens clés : `--bg: #050f1c`, `--accent: #5aacda`, dot grid, Cormorant Garamond italic h1.

### 2. Revue architecturale du frontend (analyse complète, aucun code écrit)

L'utilisateur a invoqué `/improve-codebase-architecture` sur `index.html`. **5 candidats architecturaux ont été présentés** — la session s'est terminée sans que l'utilisateur choisisse un candidat à creuser.

---

## 5 candidats architecturaux en attente de décision

### Candidat 1 — `assistant.js` monolithe (3 216 lignes) ⚠️ PRIORITÉ HAUTE

- **Problème :** 6 domaines distincts dans un fichier (rendu messages, exécution code, upload, microphone, welcome screen, thème). Interface : 6 globaux. Implémentation : 3 216 lignes. Localité nulle.
- **Solution :** Extraire `message-renderer.js`, `code-runner.js`, `file-upload.js`, `microphone.js`, `welcome-screen.js`, `theme-manager.js`. `assistant.js` devient orchestrateur ~1 200 lignes.
- **Test de délétion :** supprimer le code de rendu de `assistant.js` → la complexité réapparaît dans l'UI. Il gagne son profondeur potentielle.

### Candidat 2 — `getAuthHeaders()` dans 6 fichiers

- **Fichiers :** `assistant.js`, `account-settings.js`, `user-management.js`, `mcp-manager.js`, `mcp-tools.js`, `conversation_manager.js`
- **Solution :** Module `auth.js` exposant `getAuthHeaders()`, `getToken()`, `isAuthenticated()`.
- **Impact :** Changement auth (refresh token, rotation) en 1 seul endroit.

### Candidat 3 — Race condition initialisation

- **Fichiers :** `conversation_ui.js` (ligne ~10) vs `assistant.js` (ligne ~2216)
- **Problème :** Les deux écoutent `DOMContentLoaded`. `conversation_ui.js` dépend de `conversationManager` créé dans `assistant.js`. L'ordre n'est garanti que par la position des `<script>` dans `index.html`.
- **Solution :** Module `app-init.js` qui bootstrappe dans l'ordre et publie `app:ready`.

### Candidat 4 — Boilerplate modale × 7 fichiers

- **Fichiers :** tous les managers de modales
- **Problème :** ~50 lignes identiques (DOM cache + event binding + toggle) dans 7 modules.
- **Solution :** Factory `createModal(id, options)` ou classe `Modal`.

### Candidat 5 — Script inline `index.html` (68 lignes)

- **Lignes :** ~436–504 de `index.html`
- **Contenu :** Sidebar toggle, mode switcher, resize sync
- **Solution :** Extraire dans `ui-shell.js`, charger après `assistant.js`.

---

## Prochaines étapes suggérées

1. **Demander à l'utilisateur quel candidat creuser** (la session s'est terminée juste avant ce choix)
2. **Si candidat 2 choisi (auth.js) :** c'est le plus facile et le plus impactant à court terme — extraction pure, aucun comportement nouveau
3. **Si candidat 1 choisi (assistant.js) :** commencer par cartographier les frontières de `message-renderer.js` (la plus grande zone, ~500 lignes) avant d'écrire une ligne
4. **Commiter les changements CSS/HTML** du login-match (pas encore commités)

---

## Contexte projet

- Stack IDEA : FastAPI + pgvector + Redis + Nginx + Frontend + Langfuse self-hosted `localhost:3001`
- Sprint actif côté backend : evals plan mode (`--live` : 7/14, objectif 14/14) — voir `CLAUDE.md` dans specs
- Les changements frontend (CSS/HTML) n'affectent pas les evals backend
- ADRs existants : `docs/adr/` dans les deux repos — aucun ne concerne le frontend

## Skills à utiliser

- `/improve-codebase-architecture` — pour reprendre le grilling loop sur le candidat choisi
- `/ckm-design` — si d'autres ajustements visuels sont demandés après le choix architectural
