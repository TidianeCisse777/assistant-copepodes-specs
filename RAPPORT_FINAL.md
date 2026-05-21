# Rapport final — EcoTaxa / EcoPart probes

Date : 2026-05-19

## 1. Objectif

Tester concrètement ce qu’on peut récupérer depuis EcoTaxa et EcoPart pour préparer une exploitation de données plancton/UVP/CTD.

Deux axes ont été testés :

1. EcoTaxa LOKI `project_id = 2331`
2. Liaison EcoPart `dataset_id = 105` avec EcoTaxa `project_id = 1165`

Les tests ont distingué :

- accès public sans compte ;
- export authentifié ;
- données taxonomiques ;
- morphométrie individuelle ;
- CTD et particules agrégées ;
- faisabilité d’une jointure.

## 2. EcoTaxa LOKI — project 2331

Dossier :

```text
ecotaxa_loki_probe/
```

Projet :

```text
EcoTaxa project_id = 2331
LOKI - copepod lipids
```

Résultat :

- export authentifié réussi ;
- ZIP officiel obtenu ;
- TSV extrait ;
- 2151 objets exportés ;
- taxonomie/stade/orientation disponibles ;
- pas de mesures directes taille/poids/lipides dans l’export.

Fichiers principaux validés pendant le test, puis retirés du dépôt nettoyé :

```text
ecotaxa_loki_probe/outputs/raw/ecotaxa_loki_2331_export_job_232296.zip
ecotaxa_loki_probe/outputs/raw/export_unzipped/ecotaxa_export__TSV_2331_20260519_2055.tsv
ecotaxa_loki_probe/outputs/raw/export_columns.json
```

Fichiers conservés :

```text
ecotaxa_loki_probe/outputs/report.md
examples_tsv/loki_2331_ecotaxa_export_sample_50.tsv
```

Note : les exports bruts complets ont été retirés du dépôt nettoyé. Les exemples légers sont dans `examples_tsv/`, et les exports complets peuvent être régénérés avec les scripts.

Colonnes utiles :

```text
object_id
object_date
object_time
object_annotation_status
object_annotation_category
object_annotation_hierarchy
sample_id
sample_cruise
sample_ship
sample_stationid
classif_id
classif_auto_name
```

Taxons principaux observés :

```text
Calanus hyperboreus
Calanus glacialis
Metridia longa
Metridia
Calanus
```

Conclusion LOKI :

```text
Utilisable pour taxonomie, stade, orientation et annotations.
Pas utilisable pour taille, poids ou lipides individuels.
```

## 3. EcoPart / EcoTaxa UVP-Amundsen

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

Preuve de liaison :

```text
EcoPart sample 18027
Profile ID : ips_007
Project : uvp5_sn008_ips_amundsen_2018 (105)
Ecotaxa Project : UVP5 IPS Amundsen 2018 (1165)
Lat/Lon : 68.3094 / -60.3926
Date/Time : 2018-07-16 13:54
```

Résultat :

- liaison directe EcoPart -> EcoTaxa confirmée ;
- 7 profils EcoPart visibles ;
- EcoTaxa `1165` contient les objets individuels ;
- EcoTaxa `1165` contient la morphométrie image individuelle ;
- EcoPart `105` contient CTD, particules agrégées et plancton agrégé.

Fichiers principaux conservés :

```text
ecopart_1165_link_probe/outputs/report_ecopart_link.md
ecopart_1165_link_probe/outputs/report_join_test.md
ecopart_1165_link_probe/outputs/report_ecopart_export.md
examples_tsv/uvp_amundsen_1165_105_join_preview.tsv
examples_tsv/uvp_amundsen_105_ecopart_particles_reduced.tsv
```

Note : les réponses brutes EcoPart/EcoTaxa et ZIP complets ont été retirés du dépôt nettoyé. Les exemples TSV nécessaires sont conservés dans `examples_tsv/`.

## 4. Rôle de chaque source

### EcoTaxa 1165

Niveau :

```text
objet individuel / vignette UVP
```

Contient :

```text
object_id
sample_id
profile_id extractible depuis obj_orig_id
taxon
depth
date/time
lat/lon
area
major
minor
feret
esd
width
height
```

Exemple :

```text
obj_orig_id = ips_007_899
profile_id = ips_007
depth = 231.8
fre_area = 37.0
fre_esd = 6.86
taxon = detritus<not-living
```

### EcoPart 105

Niveau :

```text
profil / profondeur / agrégation
```

Contient :

```text
profile_id
date/time
lat/lon
depth
temperature
salinity
oxygen
fluorescence
nitrate
particle concentration
particle biovolume
plankton aggregated concentration
plankton aggregated biovolume
average ESD by category
```

## 5. Jointure testée

Jointure structurelle testée :

```text
EcoTaxa obj_orig_id = ips_007_899
        ↓
extraire profile_id = ips_007
        ↓
EcoPart profile_id = ips_007
```

Validation :

```text
Objets testés : 25
Objets reliés : 25 / 25
Dates concordantes : 25 / 25
Delta latitude max : 0.0002667
Delta longitude max : 0.0001000
```

Conclusion :

```text
La jointure profile_id est valide.
La prochaine jointure utile est profile_id + profondeur.
```

## 6. CTD et particules

Les CTD ne sont pas dans le TSV EcoTaxa.

Elles sont dans l’export EcoPart, fichier :

```text
export_reduced_20260519_21_30_PAR_Aggregated.tsv
```

Colonnes CTD disponibles :

```text
Depth [m]
temperature [degc]
practical salinity [psu]
oxygen [umol kg-1]
oxygen [ml l-1]
pressure [db]
chloro fluo [mg chl m-3]
nitrate [umol l-1]
```

Colonnes particules disponibles :

```text
LPM classes # l-1
LPM biovolume classes mm3 l-1
```

Le fichier plancton agrégé contient aussi :

```text
concentration par taxon [# m-3]
biovolume par taxon [mm3 l-1]
average ESD par taxon [mm]
```

## 7. Exemples TSV générés

Dossier :

```text
examples_tsv/
```

Fichiers :

```text
loki_2331_ecotaxa_export_sample_50.tsv
uvp_amundsen_1165_ecotaxa_object_sample.tsv
uvp_amundsen_1165_105_join_preview.tsv
uvp_amundsen_105_ecopart_particles_reduced.tsv
```

Ces 4 fichiers servent d’exemples minimaux : LOKI, objets EcoTaxa UVP, EcoPart CTD/particules, et aperçu de jointure.

## 8. Décisions

Décision 1 :

```text
LOKI 2331 est conservé comme dataset taxonomique/stade/orientation.
On abandonne la recherche de taille/poids/lipides directs dans ce projet.
```

Décision 2 :

```text
UVP-Amundsen 1165/105 est le meilleur terrain pour construire une vraie jointure EcoTaxa + EcoPart.
```

Décision 3 :

```text
EcoTaxa = objets individuels + taxonomie + morphométrie image.
EcoPart = profils + CTD + particules/plankton agrégés.
```

## 9. Prochaine étape

Construire une table jointe complète :

```text
EcoTaxa objects
  + profile_id extrait depuis obj_orig_id
  + depth objet
        ↓
EcoPart CTD/PAR/ZOO
  + profile_id
  + Depth [m]
```

Méthode :

```text
1. Charger tous les objets EcoTaxa 1165.
2. Extraire profile_id.
3. Charger EcoPart PAR_Aggregated.tsv.
4. Pour chaque objet, trouver la profondeur EcoPart la plus proche dans le même profile_id.
5. Ajouter CTD + particules à l’objet.
6. Valider les deltas de profondeur.
```

Résultat attendu :

```text
une table objet-level enrichie :
object_id
profile_id
depth
taxon
morphométrie
temperature
salinity
oxygen
fluorescence
nitrate
particle concentrations
particle biovolume
```
