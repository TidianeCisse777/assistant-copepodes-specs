# IMPLEMENTATION_ORDER.md — Ordre d'implémentation
# Assistant scientifique copépodes · NeoLab · Université Laval
#
# Principe : valider chaque fondation avant de construire dessus.
# On ne code pas de tool tant que la couche précédente n'est pas validée manuellement.
# Référence specs : TOOLS_SPEC.js · TEST_SCENARIOS.md · TOOLS_AGENT_PLAN.md

---

## PHASE A — Identité de l'agent (system prompt)

> Fondation 1 : l'agent doit savoir qui il est et ce qu'il refuse avant tout le reste.

### Ce qu'on écrit

`polar_data_tools/system_prompt.py` — une constante `COPEPOD_SYSTEM_PROMPT` (< 500 tokens) qui définit :

- **Rôle** : assistant scientifique pour données de copépodes marins (EcoTaxa / EcoPart / Amundsen CTD)
- **Utilisateurs** : Professeur et Étudiant — pas de code visible, réponses en langage naturel
- **Langue** : répond dans la langue de l'utilisateur (fr/en)
- **Refus stricts** :
  - Ne jamais inventer une citation ou une valeur numérique
  - Ne jamais lancer une analyse sans contexte scientifique (espèce, région, campagne)
  - Ne jamais exposer les credentials EcoTaxa/EcoPart
- **Ce qu'il sait faire** : décrire, lister, valider, expliquer, analyser, produire des livrables
- **Ton** : rigoureux, pédagogue, cite ses sources

### Validation

Lecture manuelle du prompt : chaque règle est vérifiable, pas de contradiction interne, tient en < 500 tokens.

**Livrable de phase :** `COPEPOD_SYSTEM_PROMPT` rédigé, relu, figé.

---

## PHASE B — Mémoire documentaire (index RAG)

> Fondation 2 : l'agent doit pouvoir répondre aux questions de domaine avant d'avoir des tools.

### Docs sources (déjà présentes)

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
| Chunking | Par section `##` (manuel) | Sections déjà autonomes, pas de découpe arbitraire par token |
| Vector store | ChromaDB local | Sans serveur, fichiers persistants, Python natif |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Léger, hors ligne, bon pour texte scientifique court |
| Retrieval | Top-3 par similarité cosinus | Suffisant pour questions colonnes et domaine |

### Scripts à créer

```
polar_data_tools/rag/
  chunk_docs.py      # découpe les 5 .md en chunks → chunks.json
  build_index.py     # embed les chunks → chroma_db/
  query.py           # rag.query(question, top_k=3) → list[Chunk]
  chunks.json        # chunks générés (committé)
  chroma_db/         # index (dans .gitignore)
```

### Validation

```python
from polar_data_tools.rag.query import query

# Test 1 — colonne instrumentale
chunks = query("que signifie acq_pixel ?")
assert any("acq_pixel" in c.content for c in chunks[:3])

# Test 2 — domaine copépodes
chunks = query("différence entre Calanus glacialis et Calanus hyperboreus")
assert any("glacialis" in c.content for c in chunks[:3])

# Test 3 — méthode de calcul
chunks = query("comment calculer le biovolume ESD ?")
assert any("biovolume" in c.content or "ESD" in c.content for c in chunks[:3])
```

**Livrable de phase :** index ChromaDB persisté, 3 requêtes de validation passent.

---

## PHASE C — Validation des connaissances (red-teaming sans tools)

> Fondation 3 : tester que prompt + RAG = un agent qui répond juste AVANT de lui donner des tools.
> Si cette phase échoue, on corrige le prompt ou l'index — on n'avance pas.

### Ce qu'on teste

Conversations manuelles (ou scripts pytest avec un LLM réel) sans aucun tool chargé.
Seuls le system prompt (Phase A) et le RAG (Phase B) sont actifs.

| Question | Comportement attendu | Scénario |
|---|---|---|
| "Que signifie acq_pixel ?" | Définition correcte depuis RAG, source citée | SC-15 |
| "C. glacialis et C. hyperboreus sont-ils identiques ?" | Avertit sur la confusion taxonomique | SC-03 |
| "Fais-moi un rapport sur les copépodes de l'Arctique" | Refuse de citer ce qu'il n'a pas en contexte | SC-06 |
| "Quelle est la concentration en copépodes ?" | Demande les données avant de répondre | SC-02 |
| Question hors domaine (météo, finance…) | Redirige poliment vers le domaine copépodes | — |

### Critères de passage

- Aucune réponse inventée (hallucination)
- Sources RAG citées quand disponibles
- Refus propres quand le contexte manque
- Ton adapté (rigoureux mais pédagogue)

**Livrable de phase :** 5 conversations validées manuellement, critères cochés.

---

## PHASE 1 — Chargement et validation des données locales

> Premier tool : l'agent peut regarder ce qu'on lui donne.

Dépend de : Phase C validée.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 1.1 | `data.inspect` | SC-13 |
| 1.2 | `data.validate` | SC-07 |
| 1.3 | `data.profile_missing` | SC-16 (partiel) |

**Fixture :** `data_exploration/examples_tsv/ecotaxa_1165_sample.tsv`

**Livrable :** on peut charger un TSV EcoTaxa, obtenir un rapport de validation structuré, vérifier que les données brutes sont préservées.

---

## PHASE 2 — Compréhension des colonnes et des sources

> L'agent peut répondre aux questions sur les données sans les avoir chargées (RAG + metadata).

Dépend de : Phase B (RAG) + Phase 1 (données chargées).

| Étape | Tool | Scénario(s) |
|---|---|---|
| 2.1 | `columns.describe` | SC-15 |
| 2.2 | `columns.check_for_calculation` | SC-01, SC-14 |
| 2.3 | `sources.list_available` | — |
| 2.4 | `sources.describe` | — |

**Livrable :** SC-01 passe (calcul refusé sans colonnes), SC-15 passe (définition correcte de acq_pixel).

---

## PHASE 3 — Contexte scientifique et mode session

> L'agent bloque toute analyse si le contexte scientifique est absent.

Dépend de : Phase 1 + Phase 2.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 3.1 | `session.set_mode` / `session.get_mode` | SC-10 |
| 3.2 | `context.get_required_fields` | SC-02 |
| 3.3 | `context.validate_species` | SC-03 |

**Livrable :** SC-02 et SC-03 passent — l'agent bloque sur contexte manquant, avertit sur C. glacialis.

---

## PHASE 4 — Interrogation des sources en ligne

> L'agent peut aller chercher des données, sans exposer les credentials.

Dépend de : Phase 3 (mode + contexte validés).

| Étape | Tool | Scénario(s) |
|---|---|---|
| 4.1 | `sources.query_amundsen_ctd` | — |
| 4.2 | `sources.query_ecotaxa` | SC-05 |
| 4.3 | `sources.query_obis` | SC-04 |

**Livrable :** SC-05 passe (credentials non exposés), SC-04 passe (absence OBIS qualifiée).

---

## PHASE 5 — Tables de travail

Dépend de : Phase 1 + Phase 4.

| Étape | Tool | Scénario(s) |
|---|---|---|
| 5.1 | `joins.plan` | SC-11 |
| 5.2 | `joins.execute` | SC-11 |

**Fixture :** `ecotaxa_1165_sample.tsv` + `ecopart_105_sample.tsv`

**Livrable :** SC-11 passe — jointure non lancée sans validation du plan.

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

**Livrable :** SC-08, SC-09, SC-01 passent complètement.

---

## PHASE 7 — Complétude et domaine

Dépend de : Phase 4 (OBIS) + Phase 1 (données locales) + Phase B (RAG).

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

**Livrable :** SC-06 passe (aucune citation inventée), SC-17 passe (résumé structuré).

---

## Graphe de dépendances

```
Phase A (system prompt)
  └── Phase B (RAG index)
        └── Phase C (red-teaming)
              └── Phase 1 (data load)
              │     └── Phase 2 (columns + sources)
              │           └── Phase 3 (context + session)
              │                 └── Phase 4 (online sources)
              │                       └── Phase 5 (joins)
              │                             └── Phase 6 (calc + analysis)
              │
              └── Phase 7 (completeness + domain)  ←── aussi Phase B + Phase 4
                    └── Phase 8 (export)
```

**Règle :** si une phase échoue à sa validation, on corrige cette phase — on n'avance pas.

---

## Récapitulatif des scénarios par phase

| Phase | Scénarios validés |
|---|---|
| A | — (validation manuelle du prompt) |
| B | — (validation manuelle du RAG) |
| C | SC-03, SC-06, SC-15 (partiel) |
| 1 | SC-07, SC-13 |
| 2 | SC-01, SC-14, SC-15 |
| 3 | SC-02, SC-03, SC-10 |
| 4 | SC-04, SC-05 |
| 5 | SC-11 |
| 6 | SC-08, SC-09 |
| 7 | SC-04, SC-12, SC-16 |
| 8 | SC-06, SC-17 |

**Tous les 17 scénarios couverts à l'issue de la Phase 8.**

---

## Structure cible du package Python

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
  fixtures/          # TSV samples depuis data_exploration/examples_tsv/
  test_system_prompt.py   # Phase A — structure et contraintes du prompt
  test_rag.py             # Phase B — chunks et retrieval
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
