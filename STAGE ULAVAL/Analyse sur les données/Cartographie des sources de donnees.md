# EcoTaxa / EcoPart / Amundsen / Données du labo

Objectif : savoir quelles données existent, où elles sont, dans quels formats, à quoi elles servent, et comment les relier.

---

## 1. Vue synthèse

|Source|Rôle|Données principales|Format|Accès|
|---|---|---|---|---|
|**EcoTaxa 2331**|Taxonomie / stade (LOKI copépodes)|taxon, stade, statut annotation, station, profondeur min/max|TSV (ZIP)|export projet 2331|
|**EcoTaxa 1165**|Morphométrie individuelle UVP5 + jointure EcoPart|object_id, obj_orig_id, area/esd/feret, profondeur, taxon|TSV (ZIP)|export projet 1165|
|**EcoPart 105**|CTD + particules agrégées par profil UVP5|profile_id, T/S/O2/fluo/nitrate, particules, plancton agrégé|TSV (bins profondeur)|EcoPart projet 105|
|**Amundsen**|Source environnementale officielle|CTD, cast_number, station, T/S/O2/fluo/nitrate|ERDDAP (CC BY 4.0)|direct ERDDAP (CTD, NAV) / on-demand (Event Log)|
|**Données du labo**|Base interne, plus proche du workflow réel|espèce, stade, longueur, lipides, condition, station, campagne|CSV principalement|fichiers directs, scripts|

---

## 2. EcoTaxa

### Projet 2331 — LOKI copepod lipids

**Rôle :** source taxonomique et de stade. Pas de morphométrie ni lipides individuels.

Export confirmé : 2151 objets.

Colonnes utiles :

```text
object_id / object_date / object_time
object_depth_min / object_depth_max    (midpoint à calculer)
object_annotation_status               V / P / D
object_annotation_category             taxon
object_annotation_hierarchy
sample_id / sample_stationid / sample_cruise / sample_ship
classif_id / classif_auto_name
```

Taxons principaux : Calanus hyperboreus, Calanus glacialis, Metridia longa, Metridia, Calanus.

Limite confirmée : pas de taille, poids ou lipides individuels dans le TSV.

### Projet 1165 — UVP5 IPS Amundsen 2018

**Rôle :** morphométrie image individuelle + jointure vers EcoPart via `obj_orig_id`.

Colonnes utiles :

```text
object_id / obj_orig_id                clé de jointure (ex: ips_007_899)
sample_id / profile_id (extrait)
depth / date / lat / lon
taxon
area / major / minor / feret / esd / width / height
```

Clé de jointure :

```text
obj_orig_id = ips_007_899 → préfixe = ips_007 → EcoPart profile_id = ips_007
```

Jointure validée : 25/25 objets reliés, dates concordantes, delta lat/lon < 0.001.

Qui comprend vraiment :

```text
biologistes, annotateurs EcoTaxa, responsable des projets
```

---

## 3. EcoPart

### Projet 105 — uvp5_sn008_ips_amundsen_2018

Lié explicitement à EcoTaxa 1165. 7 profils : ips_007 à ips_013.

Colonnes CTD disponibles :

```text
profile_id / date_time / lat / lon / depth
temperature [degc]
practical salinity [psu]
oxygen [umol kg-1] / oxygen [ml l-1]
chloro fluo [mg chl m-3]
nitrate [umol l-1]
pressure [db]
```

Colonnes particules :

```text
LPM classes # l-1
LPM biovolume classes mm3 l-1
```

Plancton agrégé :

```text
concentration par taxon [# m-3]
biovolume par taxon [mm3 l-1]
average ESD par taxon [mm]
```

Fichier principal : `export_reduced_20260519_21_30_PAR_Aggregated.tsv`

Prochaine étape : charger ce fichier et joindre par `profile_id` + profondeur la plus proche.

Qui comprend vraiment :

```text
responsable UVP, data manager, personne qui a importé dans EcoPart
```

---

## 4. Amundsen

**Rôle :** source environnementale officielle. Accès via ERDDAP (licence CC BY 4.0).

Datasets confirmés :

```text
ca-cioos_ccin-12713   CTD NGCC Amundsen          accès direct ERDDAP
ca-cioos_ccin-13248   Scientific Event Log        on-demand (formulaire), 2003-2020
ca-cioos_ccin-12447   Navigation GPS              accès direct ERDDAP
```

Colonnes CTD disponibles (ERDDAP) :

```text
platform_name / platform_id / filename
cruise_name / cruise_number / cast_number
station / time (UTC) / latitude / longitude
PRES [decibars] / depth [m]
TE90 [degC]          température
PSAL [PSU]           salinité
OXYM [uM]            oxygène
FLOR [ug/L]          fluorescence
NTRA [mmol/m^3]      nitrate
```

Clés de liaison disponibles :

```text
cast_number / station / time / lat / lon / depth    confirmes
event_id                                            absent des CTD
```

Limites :

```text
Scientific Event Log : on-demand uniquement, délai incertain.
Navigation GPS : utile seulement si lat/lon CTD/EcoPart insuffisants.
Pipeline final : URLs ERDDAP de sous-sélection à construire (cruise / station / depth range).
```

---

## 5. Données du labo

**Rôle :** données internes, base la plus proche du workflow scientifique réel.

Format attendu : CSV principalement. Possiblement aussi Excel, JSON, sorties Python/R.

Colonnes probables (noms réels inconnus) :

```text
sample_id / taxon / species / stage
body_length / lipid_volume / lipid_area / condition_index
depth / station / date_time / campaign
```

Liaison possible avec EcoTaxa :

```text
sample_id / object_id / taxon / station / date_time / depth
```

Liaison possible avec Amundsen :

```text
station / date_time / depth / campaign / event_id ou cast_id si présent
```

Qui comprend vraiment :

```text
chercheurs du labo, personne qui a produit les fichiers, personne qui lance les scripts
```

> **Point critique :** colonnes réelles inconnues. Ne pas supposer la structure. Priorité : obtenir un CSV réel, même anonymisé.

---

## 6. Liaison minimale visée

### Chemin principal — EcoTaxa 1165 ↔ EcoPart 105

Jointure structurelle validée :

```text
1. EcoTaxa obj_orig_id → extraire préfixe → profile_id (ex: ips_007)
2. EcoPart profile_id = ips_007 → CTD + particules
3. Interpoler CTD à depth = profondeur objet EcoTaxa
```

### Chemin secondaire — EcoTaxa 2331 (LOKI) ↔ Amundsen

event_id absent des CTD Amundsen. Jointure par clés contextuelles :

```text
1. sample_stationid + object_date                    réaliste
2. sample_stationid + object_date + depth midpoint   fallback utile
3. object_lat/lon + object_date + depth midpoint     fallback spatial
```

### Table V1 — objet enrichi

```text
object_id / profile_id / sample_id
taxon / stage
depth / date_time / lat / lon
area / esd / feret                     (depuis EcoTaxa 1165)
temperature / salinity / oxygen / fluorescence / nitrate
particle_concentration / particle_biovolume
match_method       (ecopart_profile | station+date | station+date+depth)
match_confidence
```