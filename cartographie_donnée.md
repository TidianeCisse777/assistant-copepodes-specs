# Cartographie des sources de donnees

Objectif : presenter clairement quelles donnees existent, ou elles sont, ce qu'elles contiennent, et comment elles peuvent etre reliees.

## 1. Vue d'ensemble

| Source | Role | Niveau | Donnees principales | Acces / format |
|---|---|---|---|---|
| EcoTaxa 2331 - LOKI | Taxonomie copépodes | objet / individu annote | taxon, stade/orientation, statut annotation, date, station, profondeur | export EcoTaxa TSV/ZIP |
| EcoTaxa 1165 - UVP5 Amundsen 2018 | Objets UVP individuels | objet / vignette image | `object_id`, `obj_orig_id`, taxon, profondeur, lat/lon, morphometrie `fre_*` | export EcoTaxa TSV/ZIP |
| EcoPart 105 | Donnees UVP agregees | profil + profondeur | `Profile`, CTD, particules, biovolumes, volume echantillonne | export EcoPart TSV |
| Amundsen Science | Environnement officiel | cast/station/profondeur | CTD officielle, navigation, `cast_number`, station, time, lat/lon, depth | ERDDAP direct ; Event Log on-demand |
| Donnees labo | Mesures biologiques internes | a confirmer | espece, stade, longueur, lipides, condition | structure inconnue tant qu'un vrai fichier n'est pas fourni |

## 2. Ce que chaque source apporte

### EcoTaxa 2331 - LOKI

- Export authentifie valide : 2151 objets.
- Utile pour taxonomie copépodes, stade/orientation et annotations.
- Limite : pas de taille, poids, lipides ou biomasse individuelle dans le TSV exporte.

Colonnes utiles :

```text
object_id
object_date / object_time Comparer ensuite avec CTD officielle Amundsen via cast/station/time/lat/lon/depth.
object_depth_min / object_depth_max
object_annotation_status
object_annotation_category / object_annotation_hierarchy
sample_id / sample_stationid / sample_cruise / sample_ship
classif_auto_name
```

### EcoTaxa 1165 - UVP5 Amundsen 2018

- Contient les objets individuels detectes par UVP.
- Donne la taxonomie/classe d'objet et la morphometrie image.
- Sert de base objet-level pour construire une table enrichie.

Colonnes utiles :

```text
object_id
obj_orig_id
sample_id
obj_depth_min / obj_depth_max
obj_objdate / obj_objtime
obj_latitude / obj_longitude
txo_display_name
fre_area / fre_esd / fre_feret / fre_major / fre_minor
```

### EcoPart 105

- Lie explicitement au projet EcoTaxa 1165.
- Donne les variables environnementales et particulaires par profil/profondeur.
- Ne decrit pas chaque objet individuellement : il faut joindre avec EcoTaxa.

Colonnes utiles :

```text
Profile
yyyy-mm-dd hh:mm
Depth [m]
temperature [degc]
practical salinity [psu]
oxygen [umol kg-1] / oxygen [ml l-1]
chloro fluo [mg chl m-3]
nitrate [umol l-1]
pressure [db]
LPM classes [# l-1]
LPM biovolume classes [mm3 l-1]
```

### Amundsen Science

- Source officielle pour les CTD et la navigation.
- CTD disponible directement via ERDDAP.
- Scientific Event Log repere, mais acces on-demand via formulaire.

Datasets confirmes :

```text
ca-cioos_ccin-12713   CTD Amundsen      ERDDAP direct
ca-cioos_ccin-12447   Navigation GPS    ERDDAP direct
ca-cioos_ccin-13248   Event Log         on-demand / formulaire
```

Colonnes CTD utiles :

```text
cast_number
station
time (UTC)
latitude / longitude
depth [m]
TE90  = temperature
PSAL  = salinity
OXYM  = oxygen
FLOR  = fluorescence
NTRA  = nitrate
```

## 3. Liaisons validees

### EcoTaxa 1165 vers EcoPart 105

La liaison structurelle fonctionne via `profile_id`.

```text
EcoTaxa obj_orig_id = ips_007_899
-> profile_id = ips_007
-> EcoPart Profile = ips_007
```

Resultat du test :

```text
25 / 25 objets relies a un profil EcoPart
dates concordantes
lat/lon coherents
```

### EcoTaxa 1165 + EcoPart 105 par profondeur

La jointure objet-level utilise :

```text
profile_id + profondeur EcoPart la plus proche
```

Resultat sur extrait :

```text
25 / 25 objets enrichis
9 objets avec match dans le bin 5 m
16 objets hors plage de profondeur de l'extrait EcoPart
```

Interpretation : la methode marche, mais l'extrait EcoPart conserve ne couvre pas toutes les profondeurs des objets.

### EcoPart 105 vers CTD officielle Amundsen

Comparaison faite sur le profil EcoPart `ips_007`.

```text
EcoPart profile_id = ips_007
Amundsen cast_number = 7
station = 1
delta temps = 3.07 min
delta latitude = 0.000200
delta longitude = 0.000100
delta profondeur median = 0.227 m
delta profondeur max = 0.484 m
```

Conclusion : EcoPart et la CTD officielle Amundsen se recoupent tres bien sur ce profil test.

## 4. Exemples TSV conserves

```text
examples_tsv/loki_2331_ecotaxa_export_sample_50.tsv
examples_tsv/uvp_amundsen_1165_ecotaxa_object_sample.tsv
examples_tsv/uvp_amundsen_105_ecopart_particles_reduced.tsv
examples_tsv/uvp_amundsen_1165_105_join_preview.tsv
examples_tsv/uvp_amundsen_1165_105_enriched_nearest_depth.tsv
examples_tsv/amundsen_12713_ctd_2018_sample.tsv
examples_tsv/amundsen_12713_ctd_ips007_match_sample.tsv
examples_tsv/uvp_amundsen_105_ecopart_vs_amundsen_ctd_compare.tsv
```

## 5. Table V1 visee

La table finale doit etre au niveau objet EcoTaxa :

```text
object_id
profile_id
sample_id
taxon
object_depth
obj_date / obj_time
obj_latitude / obj_longitude
fre_area / fre_esd / fre_feret / fre_major / fre_minor
ecopart_depth
depth_delta_m
temperature
salinity
oxygen
fluorescence
nitrate
particle_concentration
particle_biovolume
match_method
match_confidence
```

## 6. Regles de prudence

- EcoTaxa = objets/images/taxonomie/morphometrie.
- EcoPart = profils/profondeurs/CTD/particules agregees.
- Amundsen Science = source environnementale officielle.
- LOKI n'est pas encore relie a Amundsen : cette liaison reste hypothetique.
- `cast_number` existe dans Amundsen CTD ; `event_id` est absent des CTD.
- Ne pas supposer les colonnes des donnees labo avant d'avoir un vrai fichier.
- Commencer par profondeur la plus proche ; interpolation seulement ensuite si necessaire.

## 7. Priorite suivante

```text
1. Garder EcoTaxa 1165 + EcoPart 105 comme chemin principal.
2. Utiliser Amundsen CTD pour validation/enrichissement environnemental officiel.
3. Attendre un vrai fichier labo avant de modeliser les donnees biologiques internes.
```
