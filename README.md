# EcoTaxa / EcoPart exploration

Ce dépôt garde le code et les exemples propres issus des probes EcoTaxa / EcoPart.

Objectif général : comprendre quelles données sont disponibles, comment les exporter, et comment relier les objets EcoTaxa aux profils EcoPart/CTD.

## Structure

```text
.
├── CLAUDE.md                  ← point d'entrée pour Claude Code
├── CONTEXT.md                 ← glossaire domaine
├── DATA_DICTIONARY.md         ← colonnes importantes par source
├── DATA_ACCESS_METHODS.md     ← comment les données ont été obtenues
│
├── TOOLS_AGENT_PLAN.md        ← architecture du package Python (rationale)
├── TOOLS_SPEC.js              ← 22 tools : signatures, contraintes, tests A+B
├── TEST_SCENARIOS.md          ← 17 scénarios comportementaux (cas limites first)
├── IMPLEMENTATION_ORDER.md    ← 8 phases d'implémentation, Sprint 1 = Phase 0–3
│
├── docs/                      ← documents de fond (domaine, colonnes, sources)
│   ├── CONTEXT.md             ← glossaire métier
│   ├── DATA_DICTIONARY.md     ← dictionnaire des colonnes
│   ├── DATA_ACCESS_METHODS.md ← comment les données ont été obtenues
│   ├── cartographie_donnée.md ← cartographie des sources
│   └── PROJET_IDEA_ZOOPLANCTON.md ← idée initiale du projet
│
├── visualization/             ← arbre D3.js interactif (UC → Capacité → RAG)
│   ├── index.html
│   ├── data.js                ← seul fichier à modifier
│   ├── notes.js               ← brief de révision (sparse)
│   └── README.md
│
├── data_exploration/          ← scripts et données d'exploration
│   ├── examples_tsv/          ← fixtures TSV (safe to commit)
│   ├── ecotaxa_loki_probe/    ← scripts EcoTaxa 2331
│   ├── ecopart_1165_link_probe/ ← scripts jointure EcoPart 105 ↔ EcoTaxa 1165
│   └── amundsen_data_probe/   ← scripts CTD Amundsen
└── STAGE ULAVAL/              ← specs complètes (18 UC, 14 capacités, 29 contraintes)
```

## 1. LOKI EcoTaxa 2331

Dossier :

```text
ecotaxa_loki_probe/
```

Projet :

```text
EcoTaxa project_id = 2331
LOKI - copepod lipids
```

Ce qui a été validé :

- export authentifié EcoTaxa possible ;
- TSV officiel récupérable ;
- taxonomie, stade, orientation et annotations disponibles ;
- pas de taille/poids/lipides individuels directement disponibles dans ce projet.

Scripts conservés :

```text
src/export_loki_authenticated.py
src/inspect_loki_export.py
```

Rapport conservé :

```text
outputs/report.md
```

## 2. EcoPart 105 ↔ EcoTaxa 1165

Dossier :

```text
ecopart_1165_link_probe/
```

Projets liés :

```text
EcoPart dataset_id = 105
uvp5_sn008_ips_amundsen_2018

EcoTaxa project_id = 1165
UVP5 IPS Amundsen 2018
```

Ce qui a été validé :

- EcoPart pointe explicitement vers EcoTaxa `1165` ;
- EcoPart donne les profils, CTD et particules agrégées ;
- EcoTaxa donne les objets individuels, taxons et morphométrie image ;
- jointure structurelle validée via `profile_id`.

Clé de jointure :

```text
EcoTaxa obj_orig_id = ips_007_899
→ profile_id = ips_007
→ EcoPart profile_id = ips_007
```

Prochaine jointure à coder :

```text
profile_id + profondeur
```

Scripts conservés :

```text
src/probe_ecopart_1165_link.py
src/test_minimal_join.py
src/build_depth_enriched_table.py
src/export_ecopart_105_authenticated.py
```

Rapports conservés :

```text
outputs/report_ecopart_link.md
outputs/report_join_test.md
outputs/report_ecopart_export.md
```

## 3. Exemples TSV

Dossier :

```text
examples_tsv/
```

Contient des extraits légers et partageables :

```text
loki_2331_ecotaxa_export_sample_50.tsv
uvp_amundsen_1165_ecotaxa_object_sample.tsv
uvp_amundsen_1165_105_join_preview.tsv
uvp_amundsen_105_ecopart_particles_reduced.tsv
uvp_amundsen_1165_105_enriched_nearest_depth.tsv
amundsen_12713_ctd_2018_sample.tsv
amundsen_12713_ctd_ips007_match_sample.tsv
uvp_amundsen_105_ecopart_vs_amundsen_ctd_compare.tsv
```

Ces fichiers couvrent l'essentiel : LOKI, objets EcoTaxa UVP, EcoPart CTD/particules, preuve de jointure, table enrichie test, CTD officielle Amundsen, et comparaison EcoPart vs Amundsen.

## 4. Amundsen Science environnement

Dossier :

```text
amundsen_data_probe/
```

Objectif :

```text
Explorer les donnees environnementales Amundsen Science, surtout CTD-Rosette.
```

Ce qui a été validé :

- catalogue Amundsen accessible via CKAN ;
- dataset CTD `ca-cioos_ccin-12713` accessible directement via ERDDAP ;
- dataset Scientific Event Log `ca-cioos_ccin-13248` disponible via formulaire de demande ;
- dataset Navigation GPS `ca-cioos_ccin-12447` accessible via ERDDAP ;
- échantillon CTD 2018 récupéré en CSV.

Colonnes CTD utiles :

```text
cast_number
station
time
latitude / longitude
depth
TE90  = temperature
PSAL  = salinity
OXYM  = oxygen
FLOR  = fluorescence
NTRA  = nitrate
```

Rapport :

```text
amundsen_data_probe/outputs/report.md
```

## 5. Données brutes

## 5. Documentation de travail

```text
docs/cartographie_donnée.md     synthese des sources, colonnes, liaisons validees
docs/DATA_DICTIONARY.md         dictionnaire des colonnes importantes
docs/DATA_ACCESS_METHODS.md     comment les donnees ont ete obtenues et comment en faire des tools
TOOLS_AGENT_PLAN.md             architecture du package Python polar_data_tools/
TOOLS_SPEC.js                   signatures complètes des 22 tools (input/output/contraintes/tests)
TEST_SCENARIOS.md               17 scénarios comportementaux pour valider l'agent
IMPLEMENTATION_ORDER.md         ordre d'implémentation en 8 phases
```

## 6. Données brutes

Les exports complets et réponses HTML/API intermédiaires ont été retirés du dépôt nettoyé.

Ils peuvent être régénérés avec les scripts et le fichier `.env` local.

Le fichier `.env` n’est pas destiné à être partagé.

## 7. Commandes utiles

Exporter LOKI `2331` :

```bash
cd ecotaxa_loki_probe
python src/export_loki_authenticated.py
```

Tester la liaison EcoPart `105` ↔ EcoTaxa `1165` :

```bash
cd ecopart_1165_link_probe
python src/probe_ecopart_1165_link.py
python src/test_minimal_join.py
```

Exporter CTD/particules EcoPart `105` :

```bash
cd ecopart_1165_link_probe
python src/export_ecopart_105_authenticated.py
```

Explorer les donnees Amundsen Science :

```bash
cd amundsen_data_probe
python src/search_catalog.py
python src/inspect_resources.py
python src/inspect_files.py
python src/compare_ecopart_amundsen_ctd.py
```

## 8. Conclusion

LOKI `2331` est utile comme export taxonomique annoté.

Le couple EcoPart `105` / EcoTaxa `1165` est le bon terrain pour construire un dataset enrichi :

```text
objet individuel
+ taxonomie
+ morphométrie image
+ CTD
+ particules agrégées
```

La prochaine étape technique est de produire une table objet-level enrichie par jointure `profile_id + profondeur`.
