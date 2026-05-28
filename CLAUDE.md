# CLAUDE.md

## Projet

Assistant scientifique LLM+RAG+Tools pour l'exploration de données de copépodes marins.
NeoLab, Université Laval. Développeur : Flinguee75.

L'agent répond à des questions scientifiques sur des données EcoTaxa/EcoPart/Amundsen CTD
sans que l'utilisateur (Professeur ou Étudiant) ait à écrire du code.

---

Think before coding. State your assumptions out loud. If the request is ambiguous, ask. If a simpler approach exists, push back. Stop when you are confused, name what is unclear, do not just pick one interpretation and run.
Simplicity first. Write the minimum code that solves the problem. No speculative abstractions. No flexibility nobody asked for. The test: would a senior engineer call this overcomplicated.
Surgical changes. Touch only what the task requires. Do not improve neighboring code. Do not refactor what is not broken. Every changed line should trace back to the request.
Goal-driven execution. Turn vague instructions into verifiable targets before writing a line. "Add validation" becomes "write tests for invalid inputs, then make them pass."

---

## État d'avancement (mai 2026)

- Specs V1.1 complètes et figées : 18 UC, 14 capacités, 29 contraintes, 5 docs RAG
- Visualisation D3.js interactive opérationnelle (`visualization/`)
- 22 tools spécifiés avec signatures, contraintes, tests A+B (`TOOLS_SPEC.js`)
- 17 scénarios de test comportementaux documentés (`TEST_SCENARIOS.md`)
- Plan d'implémentation consolidé : `PLAN.md`

### Phases terminées dans IDEA

| Phase | Statut | Ce qui existe |
|---|---|---|
| 0 — Langfuse | ✅ | Self-hosted `localhost:3001`, observability câblée |
| A — CopepodProfile | ✅ | `agents/copepod_profile.py`, `agents/copepod_prompt.py` |
| B — RAG | ✅ | `core/copepod_rag/` (chunk, build_index, query) + ChromaDB |
| C — Red-teaming | ✅ | Evals automatisés (direct_analysis, offtopic) passent |
| 1 — Données locales | ✅ | `copepod_data.py` : inspect, infer_column_roles, describe_column |
| 2 — Colonnes + sources | ✅ | `copepod_columns.py`, `copepod_sources_meta.py` |
| 3 — Plan mode workflow | ✅ | `core/copepod_plan_workflow.py`, `copepod_session_artifacts.py` |

### Sprint actif — Evals plan mode

**Objectif :** amener le `--live` complet (Plan → Analyse) à 14/14.

**État des packs au 2026-05-27 :**

| Mode | État |
|---|---|
| `--mock` | ✅ vert |
| `--live-du-only` | ✅ vert |
| `--live-gc-only` (rich, poor, offtopic, analysis-jump) | ✅ vert |
| `--live` complet Plan → Analyse | à revalider — 7/14 au dernier run |
| Direct Analysis | ✅ 2/2 |
| Off-topic | 1/2 |
| Rejection / Retraction | à relancer en séquentiel (crash rate limit) |

**Tests `--live` qui échouent** (priorité) :
- `live_describe_column_covered_all_unmatched` — filtre pas assez strict (108 unmatched, 4 appels)
- `live_du_payload_has_column_catalogue` — `column_catalogue` vide dans le payload DU
- `live_llm_activated_data_understanding` — LLM active le DU en Phase 3 au lieu de Phase 2
- `live_llm_created_graph_context_draft_linked_to_active_du` — dépend de l'activation Phase 2
- `live_gc_payload_has_all_required_fields` — GC créé sans les champs requis
- `live_llm_activated_graph_context` — jamais activé
- `live_plan_ready_enables_analyse_mode` — `[PLAN_READY]` jamais émis

**Règle avant tout live :** toujours lancer `--mock` puis `--live-du-only` puis `--live-gc-only` avant `--live`.

### Repo IDEA

- Stack opérationnel : FastAPI + pgvector + Redis + Nginx + Frontend + Langfuse
- Langfuse self-hosted sur `http://localhost:3001` (Apple Silicon : `platform: linux/amd64`)
- Observability : `core/copepod_observability.py` — traces Langfuse par tool + phase
- **Architecture : fork IDEA** — tout le code copépode vit dans IDEA, pas un package séparé

---

## Lire avant d'implémenter quoi que ce soit

| Fichier | Contenu |
|---|---|
| `PLAN.md` | Architecture, phases, critères de test Phase 4+ |
| `docs/CONTEXT.md` | Glossaire métier |
| `TOOLS_SPEC.js` | 22 tools : signatures, contraintes (Phase 4+ non implémentées) |
| `IDEA/docs/copepod-test-operations.md` | Routine de test, niveaux, comment ajouter un test |
| `IDEA/docs/copepod-plan-mode-eval-coverage.md` | Contrat de couverture : quels checks existent et pourquoi |
| `IDEA/docs/copepod-eval-status-2026-05-27.md` | Scores par test, historique des runs |

---

## TDD — règle absolue

Pour chaque tool : écrire le test **avant** l'implémentation.
Les fixtures TSV de `data_exploration/examples_tsv/` sont la référence.
Les scénarios dans `TEST_SCENARIOS.md` définissent le comportement attendu.
Critères de passage détaillés dans `PLAN.md`.

---

## Structure réelle dans IDEA

```
IDEA/
  agents/
    copepod_profile.py         ← CopepodProfile ✅
    copepod_prompt.py          ← system prompt copépodes ✅

  core/
    copepod_rag/               ← chunk_docs.py, build_index.py, query.py ✅
    copepod_plan_workflow.py   ← machine à états DU → GC → PLAN_READY ✅
    copepod_observability.py   ← traces Langfuse par tool + phase ✅

    instruction_renderer/blocks/
      copepod_mode_plan.py     ← bloc d'instructions Plan Mode ✅
      copepod_mode_analyse.py  ← bloc d'instructions Analyse Mode ✅
      copepod_tool_signatures.py ← signatures tools injectées au LLM ✅

    tool_registry/tools/
      copepod_data.py          ← inspect, infer_column_roles, describe_column ✅
      copepod_columns.py       ← describe_column étendu, check_for_calculation ✅
      copepod_sources_meta.py  ← list_available_sources, describe_source ✅
      copepod_session_artifacts.py ← summarize_understanding, activate_data_understanding, create_graph_context, activate_graph_context ✅
      copepod_taxonomy.py      ← validate_species, get_taxonomy_context ✅
      copepod_rag.py           ← query_rag_docs (tool wrapper) ✅
      copepod_sources.py       ← query_ecotaxa, query_ecopart, ... (Phase 4 — pas encore)
      copepod_joins.py         ← join_ecotaxa_ecopart, ... (Phase 5 — pas encore)

  scripts/evals/
    run_copepod_plan_mode_eval.py      ← eval principal (GC-only + DU-only modes) ✅
    run_copepod_direct_analysis_eval.py ✅
    run_copepod_offtopic_eval.py       ✅
    run_copepod_rejection_eval.py      ✅

  tests/
    test_copepod_profile.py            ✅
    test_copepod_rag.py                ✅
    test_copepod_rag_functional.py     ✅
    test_copepod_data.py               ✅
    test_copepod_data_workflow.py      ✅
    test_copepod_columns.py            ✅
    test_copepod_sources_meta.py       ✅
    test_copepod_session_artifacts_tools.py ✅
    test_copepod_observability.py      ✅
    test_copepod_tool_observability.py ✅
    test_copepod_plan_mode_eval_runner.py ✅
    test_copepod_plan_to_analyse_integration.py ✅

  docs/
    copepod-eval-status-2026-05-27.md  ← scores + historique
    copepod-plan-mode-eval-coverage.md ← contrat de couverture
    copepod-gc-only-live-eval.md       ← guide opérationnel GC-only
    copepod-langfuse-evals.md
    copepod-test-operations.md
```

---

## Lancer les evals

```bash
# depuis IDEA/, dans Docker
docker exec -it idea-app python scripts/evals/run_copepod_plan_mode_eval.py --gc-only
docker exec -it idea-app python scripts/evals/run_copepod_plan_mode_eval.py --du-only
docker exec -it idea-app python scripts/evals/run_copepod_direct_analysis_eval.py
docker exec -it idea-app python scripts/evals/run_copepod_offtopic_eval.py

# Lancer en séquentiel pour éviter le rate limit (200k TPM)
```

---

## Sources de données

| Source | ID | Contenu |
|---|---|---|
| EcoTaxa LOKI | `2331` | Copépodes lipides, taxonomie annotée |
| EcoTaxa UVP5 | `1165` | UVP5 Amundsen 2018, objets individuels + morphométrie |
| EcoPart | `105` | UVP5 Amundsen 2018, profils CTD + particules agrégées |
| Amundsen CTD | `ca-cioos_ccin-12713` | CTD-Rosette officielle via ERDDAP |
| Données labo | *(upload utilisateur)* | Analyses lipidiques, biomasse carbone (g CO2/m³) — structure découverte à la volée via `data.inspect` |

**Clé de jointure :** `obj_orig_id` (ex. `ips_007_899`) → `profile_id` (`ips_007`) → EcoPart

---

## Visualisation

```bash
cd visualization && python3 -m http.server 8080
# → http://localhost:8080
```

- `data.js` — seul fichier à modifier (USE_CASES, CAPABILITIES, CONSTRAINTS, RAG_DOCS)
- `../TOOLS_SPEC.js` — chargé par index.html, affiche les tools dans le panneau capacité
- `notes.js` — brief de révision sparse (`ok` / `review` / `draft`)
- `visualization/README.md` — doc complète : modifier un UC, cascade d'impact, système de notes

---

## Données sensibles

`.env` contient les credentials EcoTaxa/EcoPart — jamais commité.
Scripts de régénération : `data_exploration/*/src/`.
Seuls les TSV de `data_exploration/examples_tsv/` sont commités.

---

## Structure du repo

```
CLAUDE.md                    ← ce fichier
README.md
TOOLS_SPEC.js                ← 22 tools spécifiés
TEST_SCENARIOS.md            ← 17 scénarios comportementaux

docs/
  CONTEXT.md                 ← glossaire métier, contraintes, décisions de design
  DATA_ACCESS_METHODS.md     ← comment les données ont été obtenues
  adr/                       ← décisions architecturales

data_exploration/
  examples_tsv/              ← fixtures TSV (safe to commit)
  ecotaxa_loki_probe/src/    ← scripts accès EcoTaxa 2331
  ecopart_1165_link_probe/src/ ← scripts jointure EcoPart 105 ↔ EcoTaxa 1165
  amundsen_data_probe/src/   ← scripts CTD Amundsen ERDDAP

visualization/
  index.html
  data.js
  notes.js
  README.md

STAGE ULAVAL/
  USE CASE/Use Cases — Assistant scientifique copépodes V1.md
  Agent/Spec de L'agent/Capacites agent V1.md
  Agent/Spec de L'agent/Contraintes agent V1.md
  Agent/Ressources scientifiques/Document RAG/*.md  ← 5 docs RAG sources
```
