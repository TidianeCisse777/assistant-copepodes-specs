# Dictionnaire des colonnes

Objectif : donner une definition claire des colonnes importantes pour EcoTaxa, EcoPart et Amundsen.

Niveau de confiance :

```text
officiel  = description/units disponibles dans les metadonnees de la source
observe   = colonne presente dans les exports testes
deduit    = definition deduite du nom de colonne ou du comportement observe
```

## 1. Amundsen Science CTD

Source : ERDDAP `amundsen12713`, dataset CKAN `ca-cioos_ccin-12713`.

Ces definitions viennent des metadonnees ERDDAP, donc elles sont les plus solides.

| Colonne | Definition | Unite | Confiance |
|---|---|---:|---|
| `platform_name` | Nom de la plateforme/navire | texte | officiel |
| `filename` | Fichier source CTD | texte | officiel |
| `cruise_name` | Nom de la campagne | texte | officiel |
| `cruise_number` | Numero de campagne | texte/int | officiel |
| `cast_number` | Numero de cast CTD | int | officiel |
| `station` | Station d'echantillonnage | texte | officiel |
| `time` / `time (UTC)` | Heure initiale du cast | UTC | officiel |
| `latitude` | Latitude initiale du cast | degrees_north | officiel |
| `longitude` | Longitude initiale du cast | degrees_east | officiel |
| `PRES` | Pression mesuree par le capteur CTD | decibars | officiel |
| `depth` | Profondeur | m | officiel |
| `TE90` | Temperature ITS-90 de l'eau | degC | officiel |
| `PSAL` | Salinite pratique | PSU | officiel |
| `OXYM` | Oxygene dissous | uM | officiel |
| `FLOR` | Fluorescence chlorophylle-a | ug/L | officiel |
| `NTRA` | Nitrate NO3-N | mmol/m^3 | officiel |

Equivalences utiles :

```text
TE90 = temperature
PSAL = salinity
OXYM = oxygen
FLOR = fluorescence / chlorophyll-a proxy
NTRA = nitrate
```

## 2. EcoTaxa 1165 - UVP5 Amundsen

Source : export EcoTaxa teste sur le projet `1165`.

EcoTaxa fournit surtout les objets individuels detectes sur image UVP.

| Colonne | Definition | Unite | Confiance |
|---|---|---:|---|
| `object_id` | Identifiant interne EcoTaxa de l'objet | id | observe |
| `acquisition_id` | Identifiant d'acquisition image | id | observe |
| `sample_id` | Identifiant d'echantillon EcoTaxa | id | observe |
| `project_id` | Identifiant du projet EcoTaxa | id | observe |
| `obj_orig_id` | Identifiant original de l'objet, ex. `ips_007_899` | texte | observe |
| `profile_id` | Prefixe extrait de `obj_orig_id`, ex. `ips_007` | texte | deduit |
| `obj_depth_min` | Profondeur minimum associee a l'objet | m probable | observe |
| `obj_depth_max` | Profondeur maximum associee a l'objet | m probable | observe |
| `obj_objdate` | Date de l'objet/acquisition | date | observe |
| `obj_objtime` | Heure de l'objet/acquisition | time | observe |
| `obj_latitude` | Latitude de l'objet/acquisition | degrees | observe |
| `obj_longitude` | Longitude de l'objet/acquisition | degrees | observe |
| `txo_display_name` | Taxon ou classe affichee par EcoTaxa | texte | observe |
| `fre_area` | Aire de l'objet sur l'image | pixels/units image | deduit |
| `fre_major` | Grand axe de l'objet | pixels/units image | deduit |
| `fre_minor` | Petit axe de l'objet | pixels/units image | deduit |
| `fre_feret` | Diametre de Feret, distance maximale entre deux bords | pixels/units image | deduit |
| `fre_esd` | Equivalent Spherical Diameter / diametre equivalent | pixels/units image | deduit |
| `fre_width` | Largeur de l'objet/vignette | pixels/units image | deduit |
| `fre_height` | Hauteur de l'objet/vignette | pixels/units image | deduit |

Point important :

```text
fre_* = morphometrie image, pas poids/lipides/biomasse.
```

## 3. EcoTaxa 2331 - LOKI

Source : export EcoTaxa teste sur le projet `2331`.

LOKI sert surtout pour taxonomie/stade/annotation des copépodes.

| Colonne | Definition | Unite | Confiance |
|---|---|---:|---|
| `object_id` | Identifiant EcoTaxa de l'objet | id | observe |
| `object_lat` | Latitude objet | degrees | observe |
| `object_lon` | Longitude objet | degrees | observe |
| `object_date` | Date objet/acquisition | date | observe |
| `object_time` | Heure objet/acquisition | time | observe |
| `object_depth_min` | Profondeur minimum objet | m probable | observe |
| `object_depth_max` | Profondeur maximum objet | m probable | observe |
| `object_annotation_status` | Statut d'annotation | code | observe |
| `object_annotation_category` | Categorie/taxon annote | texte | observe |
| `object_annotation_hierarchy` | Hierarchie taxonomique annotee | texte | observe |
| `sample_id` | Identifiant echantillon | id | observe |
| `sample_profileid` | Identifiant de profil si disponible | texte/id | observe |
| `sample_cruise` | Campagne | texte | observe |
| `sample_ship` | Navire | texte | observe |
| `sample_stationid` | Station | texte/id | observe |
| `classif_id` | Identifiant de classification | id | observe |
| `classif_auto_name` | Classification automatique proposee | texte | observe |
| `classif_auto_score` | Score de classification automatique | score | observe |

Limite :

```text
Pas de colonnes directes pour taille individuelle, poids, lipides ou biomasse.
```

## 4. EcoPart 105

Source : export EcoPart teste sur `uvp5_sn008_ips_amundsen_2018`.

EcoPart est au niveau profil + profondeur. Il donne CTD et particules agregees.

| Colonne | Definition | Unite | Confiance |
|---|---|---:|---|
| `Profile` | Identifiant du profil UVP, ex. `ips_007` | texte | observe |
| `Rawfilename` | Nom du fichier/source UVP | texte | observe |
| `yyyy-mm-dd hh:mm` | Date/heure du profil | datetime | observe |
| `Project` | Nom du projet EcoPart | texte | observe |
| `Depth [m]` | Profondeur du bin EcoPart | m | observe |
| `Sampled volume [L]` | Volume d'eau echantillonne | L | observe |
| `temperature [degc]` | Temperature associee au bin | degC | observe |
| `practical salinity [psu]` | Salinite pratique | psu | observe |
| `oxygen [umol kg-1]` | Oxygene dissous massique | umol kg-1 | observe |
| `oxygen [ml l-1]` | Oxygene dissous volumique | ml l-1 | observe |
| `chloro fluo [mg chl m-3]` | Fluorescence chlorophylle | mg chl m-3 | observe |
| `nitrate [umol l-1]` | Nitrate | umol l-1 | observe |
| `pressure [db]` | Pression | db | observe |
| `LPM (...) [# l-1]` | Concentration de particules par classe de taille | # l-1 | observe |
| `LPM biovolume (...) [mm3 l-1]` | Biovolume de particules par classe de taille | mm3 l-1 | observe |
| `depth [m]` | Profondeur CTD associee dans l'export | m | observe |
| `qc flag` | Indicateur qualite | code | observe |

Point important :

```text
EcoPart ne decrit pas chaque objet individuellement.
Il faut joindre EcoTaxa -> EcoPart par Profile/profile_id + profondeur proche.
```

## 5. Colonnes de jointure creees dans nos tests

Ces colonnes ne viennent pas directement des sources. Elles sont creees par les scripts.

| Colonne | Definition | Source |
|---|---|---|
| `profile_id` | Identifiant de profil extrait de `obj_orig_id` ou renomme depuis `Profile` | script |
| `object_depth` | Profondeur objet, souvent midpoint entre `obj_depth_min` et `obj_depth_max` | script |
| `ecopart_depth` | Profondeur EcoPart choisie | script |
| `depth_delta_m` | Difference absolue entre profondeur objet/EcoPart ou EcoPart/Amundsen | script |
| `depth_match_quality` | Qualite du match profondeur (`within_5m_bin`, `outside_ecopart_sample_range`, etc.) | script |
| `match_method` | Methode de jointure utilisee | script |
| `match_confidence` | Confiance prevue pour la future table V1 | concept |

## 6. Colonnes a ne pas confondre

```text
EcoTaxa object_id      = identifiant d'objet/image
EcoTaxa obj_orig_id    = identifiant original, utile pour extraire profile_id
EcoPart Profile        = profil UVP
Amundsen cast_number   = cast CTD officiel
Amundsen station       = station CTD officielle
```

```text
EcoTaxa fre_*          = morphometrie image
EcoPart LPM            = particules agregees par litre
Amundsen TE90/PSAL/... = CTD officielle
```

## 7. Limites restantes

- Les definitions Amundsen sont officielles via ERDDAP.
- Les definitions EcoTaxa/EcoPart sont observees et deduites depuis les exports.
- Il faudra chercher une documentation EcoTaxa/EcoPart plus formelle si on veut publier un schema officiel.
- Les colonnes labo restent inconnues tant qu'un vrai fichier n'est pas fourni.
