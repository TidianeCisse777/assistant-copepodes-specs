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
- Plan d'implémentation consolidé : `PLAN.md`
- **Phase 0 (Langfuse) ✅ terminée** — Sprint actif = Phase A → B → C → 1 → 2 → 3

### Repo IDEA (runtime FastAPI — séparé)

- Refactor multi-agent terminé et mergé sur `main` (42 tests verts)
- Stack complet opérationnel : FastAPI + pgvector + Redis + Nginx + Frontend + Langfuse
- Langfuse self-hosted sur `http://localhost:3001` (Apple Silicon : `platform: linux/amd64`)
- LiteLLM callback Langfuse **à câbler en Phase A**
- **Architecture : fork IDEA** — CopepodProfile + tools copépodes dans IDEA, pas un package séparé

---

## Lire avant d'implémenter quoi que ce soit

| Fichier | Contenu |
|---|---|
| `PLAN.md` | **Référence unique** : architecture, phases, critères de test |
| `TOOLS_SPEC.js` | 22 tools : signatures input/output, contraintes, tests A+B |
| `TEST_SCENARIOS.md` | 17 scénarios comportementaux (cas limites d'abord) |
| `docs/CONTEXT.md` | Glossaire métier, contraintes, décisions de design |
| `STAGE ULAVAL/USE CASE/Use Cases — Assistant scientifique copépodes V1.md` | 18 UC complets |
| `STAGE ULAVAL/Agent/Spec de L'agent/Capacites agent V1.md` | 14 capacités agent |
| `STAGE ULAVAL/Agent/Spec de L'agent/Contraintes agent V1.md` | 29 contraintes |

---

## Sprint actif — ce qui est à implémenter maintenant

**Phase A — CopepodProfile + system prompt** ← NEXT
- `IDEA/agents/copepod_profile.py` + `IDEA/utils/copepod_system_prompt.py`
- Câbler le callback LiteLLM → Langfuse dans IDEA
- Valide : 6 tests structurels verts + 4 conversations manuelles + trace Langfuse

**Phase B — RAG copépodes**
- ChromaDB sur les 5 docs `STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG/*.md`
- `IDEA/core/copepod_rag/` : chunk_docs.py → build_index.py → query.py
- Valide : 3 requêtes de test passent, chunks visibles dans Langfuse

**Phase C — Red-teaming (validation manuelle)**
- 5 conversations dans IDEA avec agent_type=copepod (SC-03, SC-06, SC-15 partiel)
- Zéro hallucination, sources RAG citées, traces Langfuse cohérentes

**Phase 1 — Données locales**
- `IDEA/core/tool_registry/tools/copepod_data.py` : inspect, validate, profile_missing
- Fixture : `data_exploration/examples_tsv/uvp_amundsen_1165_ecotaxa_object_sample.tsv`
- Valide : SC-07, SC-13

**Phase 2 — Colonnes et sources**
- `copepod_columns.py` + `copepod_sources_meta.py` dans tool registry
- `list_available_sources(auth_token)` → API dynamique, jamais hardcodé
- Valide : SC-01, SC-14, SC-15

**Phase 3 — Contexte scientifique + session**
- `session.set_mode`, `session.get_mode`, `context.get_required_fields`, `context.validate_species`
- Valide : SC-02, SC-03, SC-10

---

## TDD — règle absolue

Pour chaque tool : écrire le test **avant** l'implémentation.
Les fixtures TSV de `data_exploration/examples_tsv/` sont la référence.
Les scénarios dans `TEST_SCENARIOS.md` définissent le comportement attendu.
Critères de passage détaillés dans `PLAN.md`.

---

## Structure cible dans IDEA

```
IDEA/
  agents/
    copepod_profile.py        ← CopepodProfile (Phase A)
  utils/
    copepod_system_prompt.py  ← system prompt copépodes (Phase A)
  core/
    copepod_rag/              ← chunk_docs.py, build_index.py, query.py (Phase B)
    tool_registry/tools/
      copepod_data.py         ← inspect, validate, profile_missing (Phase 1)
      copepod_columns.py      ← describe, check_for_calculation (Phase 2)
      copepod_sources_meta.py ← list_available, describe (Phase 2)
      copepod_sources.py      ← query_ecotaxa, query_ecopart, query_amundsen_ctd, query_ogsl, query_bio_oracle (Phase 4)
      copepod_joins.py        ← join_ecotaxa_ecopart, compare_ctd_profiles (Phase 5)
  tests/
    test_copepod_profile.py   ← Phase A
    test_copepod_rag.py       ← Phase B
    test_copepod_data.py      ← Phase 1
    test_copepod_sources.py   ← Phase 4
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
