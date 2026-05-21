# Plan tools agent / MCP

Objectif : transformer les scripts d'exploration en tools reutilisables par un agent data/RAG.

Decision actuelle :

```text
Court terme : tools Python locaux.
Plus tard : MCP server si les tools deviennent stables.
```

## 1. Difference tools vs MCP

Un **tool** est une fonction appelee par l'agent.

Exemple :

```text
query_amundsen_ctd(date, lat, lon, depth_range)
```

Un **MCP server** est un serveur standardise qui expose plusieurs tools a differents agents ou applications.

```text
MCP = boite a tools partageable
Tool = fonction individuelle
```

## 2. Pourquoi commencer par des tools locaux

Les sources changent encore pendant l'exploration :

- noms de colonnes a stabiliser ;
- jointures a tester ;
- acces authentifie EcoTaxa/EcoPart ;
- sous-selections ERDDAP a affiner ;
- donnees labo encore inconnues.

Donc le bon ordre est :

```text
1. Stabiliser les fonctions Python.
2. Les tester sur les TSV exemples.
3. Les utiliser dans un agent local.
4. Emballer en MCP seulement quand les signatures sont claires.
```

## 3. Tools a brancher en premier

### amundsen.search_catalog

Cherche dans le catalogue CKAN Amundsen.

Entree :

```text
query: str
max_results: int
```

Sortie :

```text
dataset_id
title
description
license
resources
formats
urls
```

Usage :

```text
Trouver CTD, navigation, event log, datasets par annee/campagne.
```

Script source :

```text
amundsen_data_probe/src/search_catalog.py
```

### amundsen.query_ctd

Interroge ERDDAP pour obtenir un echantillon CTD.

Entree :

```text
date_start
date_end
lat_min / lat_max
lon_min / lon_max
variables
```

Sortie :

```text
DataFrame / TSV
cast_number
station
time
lat/lon
depth
TE90 / PSAL / OXYM / FLOR / NTRA
```

Usage :

```text
Recuperer CTD officielle autour d'un profil EcoPart ou d'une station.
```

Scripts sources :

```text
amundsen_data_probe/src/inspect_files.py
amundsen_data_probe/src/compare_ecopart_amundsen_ctd.py
```

### ecotaxa.inspect_export

Inspecte un export EcoTaxa TSV/ZIP.

Entree :

```text
path_to_zip_or_tsv
```

Sortie :

```text
colonnes
preview
taxons detectes
presence object_id / sample_id / depth / date / lat/lon / fre_*
```

Usage :

```text
Comprendre rapidement ce que contient un projet EcoTaxa.
```

Script source :

```text
ecotaxa_loki_probe/src/inspect_loki_export.py
```

### ecotaxa.export_project

Lance un export EcoTaxa authentifie.

Entree :

```text
project_id
with_images
auth token / env
```

Sortie :

```text
job_id
zip_path
report
```

Usage :

```text
Recuperer un TSV officiel EcoTaxa quand on a les droits.
```

Script source :

```text
ecotaxa_loki_probe/src/export_loki_authenticated.py
```

### ecopart.inspect_link

Verifie si un dataset EcoPart pointe vers un projet EcoTaxa.

Entree :

```text
ecopart_dataset_id
ecotaxa_project_id
```

Sortie :

```text
profile_id
ecopart_project
ecotaxa_project
date/time
lat/lon
link_status
```

Usage :

```text
Savoir si EcoPart a deja fait la liaison UVP -> EcoTaxa.
```

Script source :

```text
ecopart_1165_link_probe/src/probe_ecopart_1165_link.py
```

### ecopart.join_ecotaxa_by_profile

Joint les objets EcoTaxa a EcoPart par `profile_id`.

Entree :

```text
ecotaxa_objects_tsv
ecopart_profiles_or_particles_tsv
```

Sortie :

```text
object_id
obj_orig_id
profile_id
ecopart_profile_match
date_match
lat/lon deltas
```

Usage :

```text
Valider la liaison structurelle EcoTaxa -> EcoPart.
```

Script source :

```text
ecopart_1165_link_probe/src/test_minimal_join.py
```

### ecopart.enrich_by_nearest_depth

Ajoute CTD/particules EcoPart a chaque objet EcoTaxa par profondeur proche.

Entree :

```text
ecotaxa_objects_tsv
ecopart_particles_tsv
```

Sortie :

```text
object_id
profile_id
object_depth
ecopart_depth
depth_delta_m
depth_match_quality
temperature
salinity
oxygen
fluorescence
nitrate
particle summaries
```

Usage :

```text
Construire une table objet-level enrichie.
```

Script source :

```text
ecopart_1165_link_probe/src/build_depth_enriched_table.py
```

### ecopart.compare_with_amundsen_ctd

Compare EcoPart avec la CTD officielle Amundsen.

Entree :

```text
profile_id
ecopart_datetime
ecopart_lat/lon
ecopart_depths
```

Sortie :

```text
amundsen_cast_number
station
time_delta
lat/lon_delta
depth_delta
variable deltas
comparison_tsv
```

Usage :

```text
Verifier que les donnees EcoPart se recoupent avec la source officielle Amundsen.
```

Script source :

```text
amundsen_data_probe/src/compare_ecopart_amundsen_ctd.py
```

## 4. Tools plus tard

### lab.inspect_file

Pas encore codable proprement.

Il faudra d'abord un vrai fichier labo, meme anonymise.

Entree future :

```text
csv/xlsx path
```

Sortie future :

```text
colonnes
types
exemples
cles candidates
variables biologiques
```

## 5. Agent RAG cible

L'agent ne doit pas seulement chercher du texte. Il doit appeler les tools pour verifier les donnees reelles.

Flux cible :

```text
Question utilisateur
-> lire cartographie / rapports
-> appeler tool catalogue ou TSV
-> inspecter colonnes / echantillons
-> repondre avec preuves
```

Exemples :

```text
Q: A-t-on l'oxygene pour le profil ips_007 ?
Tool: ecopart.compare_with_amundsen_ctd(profile_id="ips_007")
Reponse: oui, EcoPart expose oxygen et Amundsen expose OXYM.
```

```text
Q: Comment joindre un objet UVP a la CTD ?
Tool: ecopart.enrich_by_nearest_depth(...)
Reponse: profile_id + profondeur proche, avec depth_delta_m.
```

## 6. Passage en MCP

Passer en MCP quand :

- les signatures des tools sont stables ;
- les chemins et formats sont propres ;
- on veut brancher plusieurs agents ou interfaces ;
- on veut partager les tools hors de ce repo.

Nom possible :

```text
polar_data_tools_mcp
```

Tools MCP possibles :

```text
amundsen.search_catalog
amundsen.query_ctd
ecotaxa.inspect_export
ecotaxa.export_project
ecopart.inspect_link
ecopart.enrich_by_nearest_depth
ecopart.compare_with_amundsen_ctd
```

## 7. Prochaine etape technique

Refactoriser les scripts actuels en un package Python local.

Structure cible (voir IMPLEMENTATION_ORDER.md pour l'ordre et les phases) :

```text
polar_data_tools/
  session.py        # set_mode, get_mode, build_summary, export
  context.py        # get_required_fields, validate_species
  data.py           # inspect, validate, profile_missing
  columns.py        # describe, check_for_calculation
  sources.py        # list_available, describe, query_ecotaxa,
                    # query_amundsen_ctd, query_obis
  joins.py          # plan, execute
  calc.py           # get_method, execute
  analysis.py       # explore
  plot.py           # plan, generate
  completeness.py   # evaluate, compare_obis
  domain.py         # answer
  deliverable.py    # build
  schemas.py        # types partagés : DataFrame, ValidationReport, etc.

tests/
  fixtures/         # TSV samples depuis examples_tsv/
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

Signatures complètes de chaque tool dans TOOLS_SPEC.js.
Scénarios de test comportementaux dans TEST_SCENARIOS.md.
Puis exposer ces fonctions a l'agent via MCP quand les signatures sont stables.
