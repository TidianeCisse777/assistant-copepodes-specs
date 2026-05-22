# IMPLEMENTATION_ORDER.md — Ordre d'implémentation
# Assistant scientifique copépodes · NeoLab · Université Laval
#
# Principe : valider chaque fondation avant de construire dessus.
# On ne code pas de tool tant que la couche précédente n'est pas validée manuellement.
# Référence specs : TOOLS_SPEC.js · TEST_SCENARIOS.md · TOOLS_AGENT_PLAN.md

---

## PHASE 0 — Observabilité (Langfuse) ✅ TERMINÉ (2026-05-22)

> Prérequis technique. Sans traces, débugger le RAG et les tools est aveugle.
> À faire dans IDEA avant de toucher assistant-copepodes-specs.

### Ce qui a été fait

- **Langfuse self-hosted** dans `docker-compose.yml` — service + base Postgres dédiée ✅
- **Variables `.env`** : `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` ✅
- **Compte admin + projet NeoLab/assistant-copepodes** créés dans l'UI ✅
- Fix Apple Silicon : `platform: linux/amd64` pour éviter le segfault arm64 ✅
- Port : `http://localhost:3001`

### Reste à faire (à câbler en Phase A)

- **LiteLLM callback** dans IDEA :

```python
# app.py ou core/config.py
litellm.success_callback = ["langfuse"]
```

### Ce qu'on verra dans l'interface Langfuse

| Signal | Source |
|---|---|
| Prompts envoyés + réponse LLM | LiteLLM callback automatique |
| Chunks RAG retournés (score, source) | Log structuré dans `rag/query.py` |
| Tools appelés + arguments + résultat | Log structuré dans chaque tool |
| Latence par étape | Spans Langfuse |

**Livrable :** ✅ Langfuse accessible sur `http://localhost:3001`. Callback LiteLLM à câbler en Phase A.

---

## PHASE A — Identité de l'agent (system prompt)

> Fondation 1 : l'agent sait qui il est et ce qu'il refuse.

### Ce qu'on écrit

`polar_data_tools/system_prompt.py` — constante `COPEPOD_SYSTEM_PROMPT` (< 500 tokens) :

- **Rôle** : assistant scientifique pour données copépodes marins (EcoTaxa / EcoPart / Amundsen CTD)
- **Utilisateurs** : Professeur et Étudiant — réponses en langage naturel, code généré visible et explicable
- **Langue** : répond dans la langue de l'utilisateur (fr/en)
- **Refus stricts** :
  - Ne jamais inventer une citation ou une valeur numérique
  - Ne jamais lancer une analyse sans contexte scientifique (espèce, région, campagne)
  - Ne jamais exposer les credentials EcoTaxa/EcoPart
- **Ce qu'il fait** : décrire, lister, valider, expliquer, analyser, produire des livrables
- **Ton** : rigoureux, pédagogue, cite ses sources

### Test

`tests/test_system_prompt.py` — vérifie la structure du prompt :
- Tient en < 500 tokens
- Contient les règles de refus
- Pas de contradiction interne

**Livrable :** `COPEPOD_SYSTEM_PROMPT` rédigé, testé, figé.

---

## PHASE B — Mémoire documentaire (index RAG)

> Fondation 2 : l'agent répond aux questions de domaine avant d'avoir des tools.

### Docs sources

```
STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG/
  colonnes_sources.md        (sources de données, IDs, accès)
  colonnes_instruments.md    (définitions des colonnes EcoTaxa/EcoPart)
  copepodes_domaine.md       (biologie, espèces, écologie)
  methodes_calcul.md         (biovolume, concentration, flux)
  sources_en_ligne.md        (OBIS, ERDDAP, APIs disponibles)
```

### Stack RAG

| Composant | Choix | Raison |
|---|---|---|
| Chunking | Par section `##` | Sections déjà autonomes |
| Vector store | ChromaDB local | Sans serveur, fichiers persistants |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Léger, hors ligne |
| Retrieval | Top-3 cosinus | Suffisant pour questions domaine |
| Logs | Langfuse spans | Voir les chunks retournés en temps réel |

### Scripts

```
polar_data_tools/rag/
  chunk_docs.py    # découpe les 5 .md → chunks.json
  build_index.py   # embed → chroma_db/
  query.py         # query(question, top_k=3) → list[Chunk] + log Langfuse
  chunks.json      # committé
  chroma_db/       # .gitignore
```

### Tests

```python
# tests/test_rag.py
chunks = query("que signifie acq_pixel ?")
assert any("acq_pixel" in c.content for c in chunks[:3])

chunks = query("différence Calanus glacialis / hyperboreus")
assert any("glacialis" in c.content for c in chunks[:3])

chunks = query("comment calculer le biovolume ESD ?")
assert any("biovolume" in c.content or "ESD" in c.content for c in chunks[:3])
```

**Livrable :** index persisté, 3 requêtes passent, chunks visibles dans Langfuse.

---

## PHASE C — Validation des connaissances (red-teaming)

> Fondation 3 : prompt + RAG = réponses correctes SANS tools.
> Si cette phase échoue → corriger A ou B, ne pas avancer.

### Ce qu'on teste (conversations manuelles dans IDEA)

| Question | Comportement attendu | Scénario |
|---|---|---|
| "Que signifie acq_pixel ?" | Définition depuis RAG, source citée | SC-15 |
| "C. glacialis = C. hyperboreus ?" | Avertit sur confusion taxonomique | SC-03 |
| "Fais un rapport sur les copépodes arctiques" | Refuse sans données en contexte | SC-06 |
| "Quelle est la concentration en copépodes ?" | Demande les données avant | SC-02 |
| Question hors domaine | Redirige poliment | — |

### Critères de passage

- Zéro hallucination
- Sources RAG citées quand disponibles
- Refus propres quand contexte manque
- Traces Langfuse cohérentes avec les réponses

**Livrable :** 5 conversations validées, traces Langfuse vérifiées.

---

## PHASE 1 — Chargement et validation des données locales

> Premier tool : l'agent peut inspecter ce qu'on lui donne.

Dépend de : Phase C validée.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 1.1 | `data.inspect` | SC-13 |
| 1.2 | `data.validate` | SC-07 |
| 1.3 | `data.profile_missing` | SC-16 (partiel) |

**Fixture :** `data_exploration/examples_tsv/ecotaxa_1165_sample.tsv`

**Livrable :** rapport de validation structuré, données brutes préservées.

---

## PHASE 2 — Colonnes et sources

> L'agent décrit les données sans les avoir chargées (RAG + metadata).

Dépend de : Phase B + Phase 1.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 2.1 | `columns.describe` | SC-15 |
| 2.2 | `columns.check_for_calculation` | SC-01, SC-14 |
| 2.3 | `sources.list_available` | — |
| 2.4 | `sources.describe` | — |

**Livrable :** SC-01 et SC-15 passent.

---

## PHASE 3 — Contexte scientifique et mode session

> L'agent bloque toute analyse sans contexte.

Dépend de : Phase 1 + Phase 2.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 3.1 | `session.set_mode` / `session.get_mode` | SC-10 |
| 3.2 | `context.get_required_fields` | SC-02 |
| 3.3 | `context.validate_species` | SC-03 |

**Livrable :** SC-02, SC-03, SC-10 passent.

---

## PHASE 4 — Sources en ligne

> L'agent interroge les APIs sans exposer les credentials.

Dépend de : Phase 3.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 4.1 | `sources.query_amundsen_ctd` | — |
| 4.2 | `sources.query_ecotaxa` | SC-05 |
| 4.3 | `sources.query_obis` | SC-04 |

**Livrable :** SC-04, SC-05 passent.

---

## PHASE 5 — Tables de travail

Dépend de : Phase 1 + Phase 4.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 5.1 | `joins.plan` | SC-11 |
| 5.2 | `joins.execute` | SC-11 |

**Livrable :** SC-11 passe.

---

## PHASE 6 — Calculs et analyses

Dépend de : Phase 5.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 6.1 | `calc.get_method` | SC-14 (partiel) |
| 6.2 | `calc.execute` | SC-01 |
| 6.3 | `analysis.explore` | SC-08 |
| 6.4 | `plot.plan` | — |
| 6.5 | `plot.generate` | SC-09 |

**Livrable :** SC-08, SC-09, SC-01 passent.

---

## PHASE 7 — Complétude et domaine

Dépend de : Phase 4 + Phase B + Phase 1.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 7.1 | `completeness.evaluate` | SC-16 |
| 7.2 | `completeness.compare_obis` | SC-04 |
| 7.3 | `domain.answer` | SC-06 (partiel), SC-12 |

**Livrable :** SC-04, SC-12, SC-16 passent.

---

## PHASE 8 — Export et livrables

Dépend de : toutes les phases précédentes.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 8.1 | `session.build_summary` | SC-17 |
| 8.2 | `session.export` | SC-17 |
| 8.3 | `deliverable.build` | SC-06 |

**Livrable :** SC-06, SC-17 passent.

---

## Graphe de dépendances

```
Phase 0 — Langfuse (IDEA)
  └── Phase A — System prompt
        └── Phase B — RAG index
              └── Phase C — Red-teaming (validation manuelle)
                    └── Phase 1 — Data load
                          └── Phase 2 — Columns + sources
                                └── Phase 3 — Context + session
                                      └── Phase 4 — Online sources
                                            ├── Phase 5 — Joins
                                            │     └── Phase 6 — Calc + analysis
                                            └── Phase 7 — Completeness + domain ←── Phase B
                                                  └── Phase 8 — Export
```

**Règle absolue :** si une phase échoue sa validation → corriger cette phase, ne pas avancer.

---

## Récapitulatif scénarios

| Phase | Scénarios |
|---|---|
| 0 | — (infra) |
| A | — (validation manuelle) |
| B | — (validation manuelle + Langfuse) |
| C | SC-03, SC-06, SC-15 (partiel) |
| 1 | SC-07, SC-13 |
| 2 | SC-01, SC-14, SC-15 |
| 3 | SC-02, SC-03, SC-10 |
| 4 | SC-04, SC-05 |
| 5 | SC-11 |
| 6 | SC-08, SC-09 |
| 7 | SC-04, SC-12, SC-16 |
| 8 | SC-06, SC-17 |

**17 scénarios couverts à l'issue de la Phase 8.**

---

## Structure cible du package

```
polar_data_tools/
  system_prompt.py   # COPEPOD_SYSTEM_PROMPT (Phase A)
  rag/               # chunk_docs.py, build_index.py, query.py (Phase B)
  session.py         # set_mode, get_mode, build_summary, export
  context.py         # get_required_fields, validate_species
  data.py            # inspect, validate, profile_missing
  columns.py         # describe, check_for_calculation
  sources.py         # list_available, describe, query_*
  joins.py           # plan, execute
  calc.py            # get_method, execute
  analysis.py        # explore
  plot.py            # plan, generate
  completeness.py    # evaluate, compare_obis
  domain.py          # answer
  deliverable.py     # build
  schemas.py         # types partagés

tests/
  fixtures/               # TSV depuis data_exploration/examples_tsv/
  test_system_prompt.py   # Phase A
  test_rag.py             # Phase B
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
