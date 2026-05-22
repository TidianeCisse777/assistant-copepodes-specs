# CLAUDE.md

## Projet

Assistant scientifique LLM+RAG+Tools pour l'exploration de données de copépodes marins.
NeoLab, Université Laval. Développeur : Flinguee75.

L'agent répond à des questions scientifiques sur des données EcoTaxa/EcoPart/Amundsen CTD
sans que l'utilisateur (Professeur ou Étudiant) ait à écrire du code.

---

## État d'avancement (mai 2026)

- Specs V1.1 complètes et figées : 18 UC, 14 capacités, 29 contraintes, 5 docs RAG
- Visualisation D3.js interactive opérationnelle (`visualization/`)
- 22 tools spécifiés avec signatures, contraintes, tests A+B (`TOOLS_SPEC.js`)
- 17 scénarios de test comportementaux documentés (`TEST_SCENARIOS.md`)
- Ordre d'implémentation en phases défini (`IMPLEMENTATION_ORDER.md`)
- **Phase 0 (Langfuse) ✅ terminée** — Sprint actif = Phase A → B → C → 1 → 2 → 3

### Repo IDEA (runtime FastAPI — séparé)

- Refactor multi-agent terminé et mergé sur `main` (42 tests verts)
- Stack complet opérationnel : FastAPI + pgvector + Redis + Nginx + Frontend + Langfuse
- Langfuse self-hosted sur `http://localhost:3001` (Apple Silicon : `platform: linux/amd64`)
- LiteLLM callback Langfuse **à câbler en Phase A**
- Revue archi : 9 candidats de refactor identifiés, en attente après Sprint 1
- **CopepodProfile dans IDEA = étape ultérieure**, après que `polar_data_tools` soit stable

---

## Lire avant d'implémenter quoi que ce soit

| Fichier | Contenu |
|---|---|
| `TOOLS_SPEC.js` | 22 tools : signatures input/output, contraintes, tests A+B |
| `TEST_SCENARIOS.md` | 17 scénarios comportementaux (cas limites d'abord) |
| `IMPLEMENTATION_ORDER.md` | 8 phases ordonnées, Sprint 1 = Phase 0–3 |
| `TOOLS_AGENT_PLAN.md` | Architecture du package Python, rationale |
| `STAGE ULAVAL/USE CASE/Use Cases — Assistant scientifique copépodes V1.md` | 18 UC complets |
| `STAGE ULAVAL/Agent/Spec de L'agent/Capacites agent V1.md` | 14 capacités agent |
| `STAGE ULAVAL/Agent/Spec de L'agent/Contraintes agent V1.md` | 29 contraintes |

---

## Sprint actif — ce qui est à implémenter maintenant

**Phase A — System prompt** ← NEXT
- `polar_data_tools/system_prompt.py` : `COPEPOD_SYSTEM_PROMPT` (< 500 tokens)
- Câbler le callback LiteLLM → Langfuse dans IDEA
- Valide : tests structurels + première trace visible dans Langfuse

**Phase B — Index RAG**
- Chunking des 5 docs `STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG/*.md`
- Stack : ChromaDB + sentence-transformers/all-MiniLM-L6-v2
- Scripts : `polar_data_tools/rag/chunk_docs.py` → `build_index.py` → `query.py`
- Valide : `rag.query("acq_pixel")` → bon chunk dans le top-3, chunk visible Langfuse

**Phase C — Red-teaming (validation manuelle)**
- 5 conversations de test dans IDEA (SC-03, SC-06, SC-15 partiel)
- Zéro hallucination, sources RAG citées, traces Langfuse cohérentes

**Phase 1 — Chargement et validation des données**
- `data.inspect`, `data.validate`, `data.profile_missing`
- Fixture : `data_exploration/examples_tsv/ecotaxa_1165_sample.tsv`
- Valide : SC-07, SC-13

**Phase 2 — Colonnes et sources**
- `columns.describe`, `columns.check_for_calculation`, `sources.list_available`, `sources.describe`
- Valide : SC-01, SC-14, SC-15

**Phase 3 — Contexte scientifique + session**
- `session.set_mode`, `session.get_mode`, `context.get_required_fields`, `context.validate_species`
- Valide : SC-02, SC-03, SC-10

---

## TDD — règle absolue

Pour chaque tool : écrire le test pytest **avant** l'implémentation.
Les tests s'appuient sur les fixtures TSV de `data_exploration/examples_tsv/`.
Les scénarios dans `TEST_SCENARIOS.md` définissent le comportement attendu.
Chaque "Signe d'échec" = assertion Python concrète.

---

## Structure cible du package Python

```
polar_data_tools/
  rag/             # chunk_docs.py, build_index.py, query.py, chunks.json
  session.py       # set_mode, get_mode, build_summary, export
  context.py       # get_required_fields, validate_species
  data.py          # inspect, validate, profile_missing
  columns.py       # describe, check_for_calculation
  sources.py       # list_available, describe, query_ecotaxa,
                   # query_amundsen_ctd, query_obis
  joins.py         # plan, execute
  calc.py          # get_method, execute
  analysis.py      # explore
  plot.py          # plan, generate
  completeness.py  # evaluate, compare_obis
  domain.py        # answer
  deliverable.py   # build
  schemas.py       # types partagés

tests/
  fixtures/        # symlinks ou copies depuis data_exploration/examples_tsv/
  test_session.py
  test_context.py
  test_data.py
  test_columns.py
  test_sources.py
  test_joins.py
  test_calc.py
  test_analysis.py
  test_completeness.py
  test_domain.py
  test_deliverable.py
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
IMPLEMENTATION_ORDER.md      ← 8 phases
TOOLS_AGENT_PLAN.md          ← architecture Python

docs/
  CONTEXT.md                 ← glossaire métier
  DATA_ACCESS_METHODS.md     ← comment les données ont été obtenues

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
