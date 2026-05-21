# IMPLEMENTATION_ORDER.md — Ordre d'implémentation
# Assistant scientifique copépodes · NeoLab · Université Laval
#
# Principe : chaque phase débloque la suivante.
# Référence specs : TOOLS_SPEC.js · TEST_SCENARIOS.md · TOOLS_AGENT_PLAN.md
# TDD : pour chaque tool, écrire le test pytest AVANT l'implémentation.

---

## PHASE 0 — Infrastructure session (déblocage global)

> Rien ne fonctionne sans session state et mode actif.

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 0.1 | `session.set_mode` | SC-10 |
| 0.2 | `session.get_mode` | SC-10 |
| 0.3 | `context.get_required_fields` | SC-02 |

**Livrable de phase :** on peut activer un mode, vérifier qu'il bloque l'analyse sans contexte.

---

## PHASE 1 — Chargement et validation des données locales

> Fondation de toutes les analyses. Couvre les UC-SL-03/05/06.

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 1.1 | `data.inspect` | SC-13 |
| 1.2 | `data.validate` | SC-07 |
| 1.3 | `data.profile_missing` | SC-16 (partiel) |

**Fixture de test :** `examples_tsv/ecotaxa_1165_sample.tsv`

**Livrable de phase :** on peut charger un TSV EcoTaxa, obtenir un rapport de validation structuré, vérifier que les données brutes sont préservées.

---

## PHASE 2 — Compréhension des sources et des colonnes

> Couche RAG — répondre aux questions sur les données sans les charger.

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 2.1 | `columns.describe` | SC-15 |
| 2.2 | `columns.check_for_calculation` | SC-01, SC-14 |
| 2.3 | `sources.list_available` | — |
| 2.4 | `sources.describe` | — |

**Livrable de phase :** SC-01 passe (calcul refusé sans colonnes), SC-15 passe (définition de acq_pixel correcte).

---

## PHASE 3 — Contexte scientifique

> Bloque toutes les analyses si absent. Priorité haute.

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 3.1 | `context.validate_species` | SC-03 |
| 3.2 | Intégration `context.get_required_fields` → mode Analyse | SC-02, SC-10 |

**Livrable de phase :** SC-02 et SC-03 passent — l'agent bloque sur contexte manquant, avertit sur C. glacialis.

---

## PHASE 4 — Interrogation des sources en ligne

> Dépend de Phase 0 (mode) et Phase 2 (sources connues).

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 4.1 | `sources.query_amundsen_ctd` | — |
| 4.2 | `sources.query_ecotaxa` | SC-05 |
| 4.3 | `sources.query_obis` | SC-04 |

**Livrable de phase :** SC-05 passe (credentials non exposés), SC-04 passe (absence OBIS qualifiée).

---

## PHASE 5 — Construction des tables de travail

> Dépend de Phase 1 (données chargées et validées).

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 5.1 | `joins.plan` | SC-11 |
| 5.2 | `joins.execute` | SC-11 |

**Fixture de test :** `examples_tsv/ecotaxa_1165_sample.tsv` + `examples_tsv/ecopart_105_sample.tsv`

**Livrable de phase :** SC-11 passe — jointure non lancée sans validation du plan.

---

## PHASE 6 — Calculs et analyses

> Dépend de Phase 5 (table de travail disponible).

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 6.1 | `calc.get_method` | SC-14 (partiel) |
| 6.2 | `calc.execute` | SC-01 |
| 6.3 | `analysis.explore` | SC-08 |
| 6.4 | `plot.plan` | — |
| 6.5 | `plot.generate` | SC-09 |

**Livrable de phase :** SC-08 passe (observation/interprétation séparées), SC-09 passe (graphique avec source), SC-01 passe complètement.

---

## PHASE 7 — Complétude et domaine

> Dépend de Phase 4 (OBIS) et Phase 1 (données locales).

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 7.1 | `completeness.evaluate` | SC-16 |
| 7.2 | `completeness.compare_obis` | SC-04 |
| 7.3 | `domain.answer` | SC-06 (partiel), SC-12 |

**Livrable de phase :** SC-04, SC-12, SC-16 passent.

---

## PHASE 8 — Export et livrables

> Dépend de toutes les phases précédentes.

| Étape | Tool | Scénario(s) validé(s) |
|---|---|---|
| 8.1 | `session.build_summary` | SC-17 |
| 8.2 | `session.export` | SC-17 |
| 8.3 | `deliverable.build` | SC-06 |

**Livrable de phase :** SC-06 passe (aucune citation inventée), SC-17 passe (résumé structuré sans narration).

---

## Récapitulatif des scénarios par phase

| Phase | Scénarios débloqués |
|---|---|
| 0 | SC-10 (partiel) |
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
  schemas.py       # types partagés : DataFrame, ValidationReport, etc.

tests/
  fixtures/        # TSV samples depuis examples_tsv/
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
