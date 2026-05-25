# Acces aux donnees et construction des futurs tools

Objectif : documenter comment les donnees EcoTaxa, EcoPart et Amundsen ont ete obtenues, afin de transformer ces acces en tools reutilisables.

## 1. Principe general

Les probes ne font pas de scraping massif.

La logique utilisee :

```text
1. Identifier une source officielle.
2. Tester l'acces public ou authentifie.
3. Telecharger seulement metadata ou petits echantillons.
4. Sauvegarder les reponses utiles.
5. Inspecter colonnes, formats, unites et cles de liaison.
6. Produire un rapport et des TSV exemples.
```

## 2. EcoTaxa

### Acces teste

Sources :

```text
https://ecotaxa.obs-vlfr.fr/prj/{project_id}
https://ecotaxa.obs-vlfr.fr/api/docs
POST /object_set/{project_id}/query
POST /object_set/export/general
GET  /api/jobs/{job_id}/file
```

Projets testes :

```text
2331  LOKI - copepod lipids
1165  UVP5 IPS Amundsen 2018
42    UVP5 GREEN EDGE Ice Camp 2015
```

### Acces sans compte

La page projet peut etre visible publiquement selon le projet.

Mais pour obtenir un export TSV complet, le chemin utile est l'API authentifiee.

### Acces avec compte

Les identifiants ne sont pas stockes dans le repo.

La configuration passe par `.env` local :

```text
ECOTAXA_USERNAME=
ECOTAXA_PASSWORD=
ECOTAXA_TOKEN=
```

Le fichier `.env` est ignore et ne doit pas etre partage.

### Export EcoTaxa

Flux observe :

```text
1. Charger credentials depuis .env.
2. S'authentifier ou utiliser ECOTAXA_TOKEN.
3. Appeler POST /object_set/export/general.
4. Recuperer un job_id.
5. Poller le job jusqu'a completion.
6. Telecharger GET /api/jobs/{job_id}/file.
7. Dezipper le fichier si ZIP.
8. Inspecter le TSV.
```

Script source :

```text
ecotaxa_loki_probe/src/export_loki_authenticated.py
ecotaxa_green_edge_probe/src/export_green_edge_authenticated.py
```

Inspection :

```text
ecotaxa_loki_probe/src/inspect_loki_export.py
ecotaxa_green_edge_probe/src/inspect_green_edge_export.py
```

### Donnees obtenues

Projet LOKI `2331` :

```text
TSV officiel exporte
2151 objets
taxonomie / stade / orientation / annotation
pas de poids, lipides, biomasse individuelle
```

Projet UVP5 `1165` :

```text
objets individuels UVP
obj_orig_id
profondeur
date/time
lat/lon
taxon / classe objet
morphometrie image fre_*
```

Projet UVP5 GREEN EDGE Ice Camp 2015 `42` :

```text
page projet publique confirmee
export authentifie prepare via API EcoTaxa
sorties isolees dans ecotaxa_green_edge_probe/outputs/
```

### Implication pour tools

Tools a construire :

```text
ecotaxa.inspect_project(project_id)
ecotaxa.export_project(project_id, with_images=False)
ecotaxa.inspect_export(path)
ecotaxa.extract_profile_id(obj_orig_id)
```

Sorties attendues :

```text
colonnes
preview
taxons
presence fre_*
presence profondeur/date/lat/lon
chemin TSV extrait
```

## 3. EcoPart

### Acces teste

Source :

```text
https://ecopart.obs-vlfr.fr
```

Dataset teste :

```text
EcoPart dataset_id = 105
uvp5_sn008_ips_amundsen_2018
```

Projet EcoTaxa lie :

```text
EcoTaxa project_id = 1165
UVP5 IPS Amundsen 2018
```

### Verification de la liaison EcoPart -> EcoTaxa

Le lien a ete verifie via les informations de profil/sample EcoPart.

Exemple valide :

```text
EcoPart sample 18027
Profile ID = ips_007
Project = uvp5_sn008_ips_amundsen_2018 (105)
Ecotaxa Project = UVP5 IPS Amundsen 2018 (1165)
Lat/Lon = 68.3094 / -60.3926
Date/Time = 2018-07-16 13:54
```

Script source :

```text
ecopart_1165_link_probe/src/probe_ecopart_1165_link.py
```

### Export EcoPart

Un export authentifie EcoPart a ete teste pour obtenir CTD/particules.

Script source :

```text
ecopart_1165_link_probe/src/export_ecopart_105_authenticated.py
```

Les fichiers bruts complets ont ete retires du repo nettoye.

Un extrait conserve :

```text
examples_tsv/uvp_amundsen_105_ecopart_particles_reduced.tsv
```

### Donnees obtenues

EcoPart donne des donnees par profil/profondeur :

```text
Profile
Depth [m]
yyyy-mm-dd hh:mm
temperature
salinity
oxygen
fluorescence
nitrate
pressure
sampled volume
particle concentration by size class
particle biovolume by size class
```

### Jointure EcoTaxa -> EcoPart

Principe :

```text
EcoTaxa obj_orig_id = ips_007_899
-> extraire profile_id = ips_007
-> joindre avec EcoPart Profile = ips_007
```

Puis :

```text
object_depth
-> EcoPart Depth [m] le plus proche dans le meme Profile
```

Scripts sources :

```text
ecopart_1165_link_probe/src/test_minimal_join.py
ecopart_1165_link_probe/src/build_depth_enriched_table.py
```

Resultats :

```text
25/25 objets relies au profil EcoPart sur l'extrait
9/25 objets avec match profondeur dans le bin 5 m
16/25 hors plage de profondeur de l'extrait EcoPart
```

### Implication pour tools

Tools a construire :

```text
ecopart.inspect_dataset(dataset_id)
ecopart.inspect_link(dataset_id, ecotaxa_project_id)
ecopart.export_dataset(dataset_id)
ecopart.join_ecotaxa_by_profile(ecotaxa_tsv, ecopart_tsv)
ecopart.enrich_by_nearest_depth(ecotaxa_tsv, ecopart_tsv)
```

Sorties attendues :

```text
profile_id
date/time
lat/lon
ecotaxa_project_id lie
colonnes CTD/particules
depth_delta_m
depth_match_quality
```

## 4. Amundsen Science

### Acces teste

Catalogue :

```text
https://catalogue.amundsenscience.com
```

Le catalogue est base sur CKAN.

API utilisee :

```text
GET /api/3/action/package_search
GET /api/3/action/package_show
```

Scripts sources :

```text
amundsen_data_probe/src/search_catalog.py
amundsen_data_probe/src/inspect_resources.py
```

### Datasets identifies

```text
ca-cioos_ccin-12713   CTD Amundsen       ERDDAP direct
ca-cioos_ccin-12447   Navigation GPS     ERDDAP direct
ca-cioos_ccin-13248   Event Log          formulaire / on-demand
```

### Acces CTD via ERDDAP

Dataset ERDDAP :

```text
https://erddap.amundsenscience.com/erddap/tabledap/amundsen12713
```

Metadonnees variables :

```text
https://erddap.amundsenscience.com/erddap/info/amundsen12713/index.csv
```

Exemple de requete CSV :

```text
https://erddap.amundsenscience.com/erddap/tabledap/amundsen12713.csvp?
platform_name,filename,cruise_name,cruise_number,cast_number,station,time,latitude,longitude,PRES,depth,TE90,PSAL,OXYM,FLOR,NTRA
&time>=2018-07-16T00:00:00Z
&time<=2018-07-16T23:59:59Z
&latitude>=68.0
&latitude<=68.6
&longitude>=-60.8
&longitude<=-60.0
```

Script source :

```text
amundsen_data_probe/src/compare_ecopart_amundsen_ctd.py
```

### Donnees obtenues

Colonnes CTD officielles :

```text
cast_number
station
time
latitude / longitude
PRES
depth
TE90 = temperature
PSAL = salinity
OXYM = oxygen
FLOR = fluorescence
NTRA = nitrate
```

Les definitions et unites viennent directement des metadonnees ERDDAP.

### Comparaison EcoPart -> Amundsen

Profil teste :

```text
EcoPart Profile = ips_007
EcoPart time = 2018-07-16 13:54:01
EcoPart lat/lon = 68.3094 / -60.3926
```

Cast Amundsen trouve :

```text
cast_number = 7
station = 1
time = 2018-07-16T13:57:04Z
lat/lon = 68.3096 / -60.3925
```

Ecarts :

```text
delta temps = 3.07 min
delta latitude = 0.000200
delta longitude = 0.000100
delta profondeur median = 0.227 m
delta profondeur max = 0.484 m
```

Conclusion :

```text
EcoPart et Amundsen CTD officielle se recoupent tres bien sur ce profil test.
La generalisation doit appliquer la meme logique a tous les profils.
```

### Implication pour tools

Tools a construire :

```text
amundsen.search_catalog(query)
amundsen.get_dataset(dataset_id)
amundsen.get_erddap_metadata(dataset_id)
amundsen.query_ctd(date_range, lat_range, lon_range, variables)
amundsen.compare_with_ecopart(profile_metadata, ecopart_depths)
```

Sorties attendues :

```text
dataset metadata
resource URLs
variable dictionary
CTD sample
matching cast_number/station
time/lat/lon/depth deltas
```

## 5. Organisation actuelle des preuves

Rapports :

```text
docs/REPO_GUIDE.md
docs/FOLDER_MAP.md
docs/CONTEXT.md
docs/DATA_ACCESS_METHODS.md
TOOLS_SPEC.js
TEST_SCENARIOS.md
ecopart_1165_link_probe/outputs/report_depth_enriched_table.md
amundsen_data_probe/outputs/report_ecopart_amundsen_compare.md
```

TSV exemples :

```text
examples_tsv/ecotaxa_sample_50.tsv
examples_tsv/uvp_amundsen_1165_ecotaxa_object_sample.tsv
examples_tsv/uvp_amundsen_105_ecopart_particles_reduced.tsv
examples_tsv/uvp_amundsen_1165_105_join_preview.tsv
examples_tsv/uvp_amundsen_1165_105_enriched_nearest_depth.tsv
examples_tsv/amundsen_12713_ctd_2018_sample.tsv
examples_tsv/amundsen_12713_ctd_ips007_match_sample.tsv
examples_tsv/uvp_amundsen_105_ecopart_vs_amundsen_ctd_compare.tsv
```

## 6. Limites et prudence

- Les credentials EcoTaxa/EcoPart ne doivent pas etre commits.
- Les exports complets ont ete retires du repo nettoye.
- Les exemples TSV sont faits pour comprendre les formats, pas pour produire une analyse scientifique finale.
- EcoPart/EcoTaxa peuvent necessiter une session authentifiee selon les projets et exports.
- Amundsen CTD est le chemin le plus propre car ERDDAP fournit des metadonnees officielles.

## 7. Passage vers tools

La prochaine etape technique est de sortir la logique des scripts vers un package :

```text
IDEA/core/tool_registry/tools/  ← cible d'implémentation des tools
```

Signatures complètes des tools : TOOLS_SPEC.js.
Scénarios de test comportementaux : TEST_SCENARIOS.md.
Plan d'implémentation consolidé : PLAN.md.

Le MCP viendra ensuite si les signatures sont stables.
