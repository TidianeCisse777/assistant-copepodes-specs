# Definitions des colonnes conservees

Dataset : EcoTaxa projet 42, UVP5 GREEN EDGE Ice Camp 2015.
Lignes : 84668
Colonnes conservees : 122
Colonnes supprimees : 39

Regle de nettoyage : suppression des colonnes toujours nulles, constantes, ou tres sparse avec une seule valeur non nulle dans le TSV exporte.

Note : les mesures `object_*` de morphometrie sont en pixels sauf indication contraire. Pour convertir une longueur en mm, multiplier par `acq_pixel`.

## objet/identification

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_id` | Identifiant unique de l objet dans EcoTaxa, construit depuis acquisition + numero objet. | id | 0.0% | 84668 |

## objet/spatial

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_lat` | Latitude de l objet ou du profil associe. | degres decimaux | 0.0% | 2 |
| `object_lon` | Longitude de l objet ou du profil associe. | degres decimaux | 0.0% | 2 |

## objet/temps

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_date` | Date UTC d echantillonnage ou acquisition. | date | 0.0% | 30 |
| `object_time` | Heure UTC d echantillonnage ou acquisition. | heure | 0.0% | 32 |

## objet/profondeur

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_depth_min` | Profondeur minimale associee a l objet. | m | 0.0% | 3575 |
| `object_depth_max` | Profondeur maximale associee a l objet. Utiliser le midpoint avec object_depth_min. | m | 0.0% | 3575 |

## annotation/taxonomie

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_annotation_category` | Categorie ou taxon valide affiche par EcoTaxa. Champ principal pour les analyses taxonomiques. | texte | 0.0% | 39 |
| `object_annotation_hierarchy` | Hierarchie taxonomique complete associee a la categorie annotee. | texte | 0.0% | 39 |

## annotation/audit

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_annotation_person_name` | Nom de la personne ayant valide l annotation. | texte | 0.0% | 15 |
| `object_annotation_person_email` | Email de la personne ayant valide l annotation. Donnee personnelle, a eviter dans les exports publics. | texte | 0.0% | 15 |
| `object_annotation_date` | Date de validation ou modification de l annotation. | date | 0.0% | 40 |
| `object_annotation_time` | Heure de validation ou modification de l annotation. | heure | 0.0% | 2086 |

## morphometrie

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `object_area` | Surface de l objet. | pixel2 | 0.0% | 5248 |
| `object_mean` | Niveau de gris moyen de l objet. | 0-255 | 0.0% | 6328 |
| `object_stddev` | Ecart-type des niveaux de gris. | niveau de gris | 0.0% | 25951 |
| `object_mode` | Mode des niveaux de gris. | 0-255 | 0.0% | 102 |
| `object_min` | Niveau de gris minimum. | 0-255 | 0.0% | 234 |
| `object_max` | Niveau de gris maximum. | 0-255 | 0.0% | 8 |
| `object_x` | Coordonnee x du centroide ou de reference objet dans l image. | pixel | 0.0% | 10412 |
| `object_y` | Coordonnee y du centroide ou de reference objet dans l image. | pixel | 0.0% | 7135 |
| `object_xm` | Coordonnee x du centre de masse en niveaux de gris. | pixel | 0.0% | 10367 |
| `object_ym` | Coordonnee y du centre de masse en niveaux de gris. | pixel | 0.0% | 7139 |
| `object_perim.` | Perimetre externe de l objet. | pixel | 0.0% | 9515 |
| `object_bx` | Coordonnee x du rectangle englobant. | pixel | 0.0% | 183 |
| `object_by` | Coordonnee y du rectangle englobant. | pixel | 0.0% | 137 |
| `object_width` | Largeur du rectangle englobant. | pixel | 0.0% | 219 |
| `object_height` | Hauteur du rectangle englobant. | pixel | 0.0% | 185 |
| `object_major` | Grand axe de l ellipse ajustee. | pixel | 0.0% | 1410 |
| `object_minor` | Petit axe de l ellipse ajustee. | pixel | 0.0% | 1027 |
| `object_angle` | Angle de l axe principal de l objet. | degres | 0.0% | 1801 |
| `object_circ.` | Circularite de l objet, 1 etant proche d un cercle parfait. | sans unite | 0.0% | 972 |
| `object_feret` | Diametre de Feret, longueur maximale de l objet. | pixel | 0.0% | 1425 |
| `object_intden` | Densite integree, approximativement surface x intensite moyenne. | intensite*pixel2 | 0.0% | 47493 |
| `object_median` | Mediane des niveaux de gris. | 0-255 | 0.0% | 91 |
| `object_skew` | Asymetrie de la distribution des niveaux de gris. | sans unite | 0.0% | 5828 |
| `object_kurt` | Kurtosis de la distribution des niveaux de gris. | sans unite | 0.0% | 13899 |
| `object_%area` | Pourcentage de surface occupee par l objet. | % | 0.0% | 2796 |
| `object_xstart` | Position x de depart de la vignette ou ROI. | pixel | 0.0% | 255 |
| `object_ystart` | Position y de depart de la vignette ou ROI. | pixel | 0.0% | 137 |
| `object_area_exc` | Surface de l objet en excluant les trous. | pixel2 | 0.0% | 866 |
| `object_fractal` | Dimension fractale du contour. | sans unite | 0.0% | 944 |
| `object_skelarea` | Surface ou longueur du squelette de l objet. | pixel2 | 0.0% | 2127 |
| `object_slope` | Pente de l histogramme cumule normalise. | sans unite | 0.0% | 2376 |
| `object_histcum1` | Premier quartile de l histogramme cumule des niveaux de gris. | 0-255 | 0.0% | 224 |
| `object_histcum2` | Deuxieme quartile de l histogramme cumule des niveaux de gris. | 0-255 | 0.0% | 94 |
| `object_histcum3` | Troisieme quartile de l histogramme cumule des niveaux de gris. | 0-255 | 0.0% | 26 |
| `object_nb1` | Nombre de pixels ou composante dans la classe de gris 1. | nombre | 0.0% | 47 |
| `object_nb2` | Nombre de pixels ou composante dans la classe de gris 2. | nombre | 0.0% | 67 |
| `object_nb3` | Nombre de pixels ou composante dans la classe de gris 3. | nombre | 0.0% | 80 |
| `object_symetrieh` | Indice de symetrie horizontale. | sans unite | 0.0% | 5856 |
| `object_symetriev` | Indice de symetrie verticale. | sans unite | 0.0% | 5848 |
| `object_symetriehc` | Indice derive de symetrie horizontale corrigee. | sans unite | 0.0% | 35 |
| `object_symetrievc` | Indice derive de symetrie verticale corrigee. | sans unite | 0.0% | 37 |
| `object_convperim` | Perimetre de l enveloppe convexe. | pixel | 0.0% | 554 |
| `object_convarea` | Surface de l enveloppe convexe. | pixel2 | 0.0% | 5719 |
| `object_fcons` | Indice de contraste ou texture. | sans unite | 0.0% | 15094 |
| `object_thickr` | Ratio d epaisseur maximale sur epaisseur moyenne. | sans unite | 0.0% | 5222 |
| `object_areai` | Surface ou aire integree derivee. | pixel2 | 0.0% | 4790 |
| `object_esd` | Diametre equivalent sphérique calcule depuis la surface. | pixel | 0.0% | 5536 |
| `object_elongation` | Indice d elongation, typiquement major/minor. | sans unite | 0.0% | 2087 |
| `object_range` | Etendue des niveaux de gris. | 0-255 | 0.0% | 238 |
| `object_meanpos` | Position moyenne ponderee par les niveaux de gris. | pixel | 0.0% | 33901 |
| `object_centroids` | Distance entre centroide geometrique et centroide d intensite. | pixel | 0.0% | 14 |
| `object_cv` | Coefficient de variation des niveaux de gris. | % | 0.0% | 23684 |
| `object_sr` | Descripteur derive de texture/forme Zooprocess. | sans unite | 0.0% | 3227 |
| `object_perimareaexc` | Ratio ou derive combinant perimetre et surface sans trous. | sans unite | 53.5% | 13114 |
| `object_feretareaexc` | Ratio ou derive combinant Feret et surface sans trous. | sans unite | 53.5% | 8547 |
| `object_perimferet` | Ratio ou derive combinant perimetre et Feret. | sans unite | 0.0% | 7797 |
| `object_perimmajor` | Ratio ou derive combinant perimetre et grand axe. | sans unite | 0.0% | 7869 |
| `object_circex` | Circularite calculee sur la surface sans trous. | sans unite | 0.0% | 13323 |
| `object_cdexc` | Descripteur derive de compacite/circularite sans trous. | sans unite | 53.5% | 508 |
| `object_kurt_mean` | Ratio ou derive combinant kurtosis et gris moyen. | sans unite | 4.3% | 21144 |
| `object_skew_mean` | Ratio ou derive combinant skewness et gris moyen. | sans unite | 4.3% | 12761 |
| `object_convperim_perim` | Ratio perimetre convexe / perimetre. | sans unite | 4.3% | 10057 |
| `object_convarea_area` | Ratio surface convexe / surface. | sans unite | 4.3% | 22109 |
| `object_symetrieh_area` | Symetrie horizontale normalisee par la surface. | sans unite | 4.3% | 7587 |
| `object_symetriev_area` | Symetrie verticale normalisee par la surface. | sans unite | 4.3% | 7566 |
| `object_nb1_area` | Classe nb1 normalisee par la surface. | sans unite | 4.3% | 5670 |
| `object_nb2_area` | Classe nb2 normalisee par la surface. | sans unite | 4.3% | 7590 |
| `object_nb3_area` | Classe nb3 normalisee par la surface. | sans unite | 4.3% | 7992 |
| `object_nb1_range` | Classe nb1 normalisee par l etendue de gris. | sans unite | 4.3% | 953 |
| `object_nb2_range` | Classe nb2 normalisee par l etendue de gris. | sans unite | 4.3% | 1156 |
| `object_nb3_range` | Classe nb3 normalisee par l etendue de gris. | sans unite | 4.3% | 1153 |
| `object_median_mean` | Ratio mediane / moyenne des niveaux de gris. | sans unite | 4.3% | 4220 |
| `object_median_mean_range` | Ratio mediane/moyenne normalise par l etendue de gris. | sans unite | 4.3% | 28023 |
| `object_skeleton_area` | Squelette normalise par la surface. | sans unite | 4.3% | 20440 |

## sample

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `sample_id` | Identifiant du sample EcoTaxa. | id | 0.0% | 32 |
| `sample_profileid` | Identifiant du profil ou dossier brut de la sequence UVP5. | texte | 0.0% | 32 |
| `sample_comment` | Commentaire terrain ou traitement associe au sample. | texte | 0.0% | 4 |

## sample/spatial

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `sample_lat` | Latitude du sample. | degres decimaux | 0.0% | 2 |
| `sample_long` | Longitude du sample. | degres decimaux | 0.0% | 2 |

## sample/ctd

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `sample_ctdrosettefilename` | Nom du fichier CTD rosette associe au sample. | texte | 0.0% | 30 |

## sample/meteo

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `sample_windspeed` | Vitesse du vent renseignee au niveau sample. | noeuds | 0.0% | 3 |
| `sample_nebuloussness` | Nebulosite renseignee au niveau sample. | octa | 0.0% | 8 |

## process

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `process_id` | Identifiant du traitement Zooprocess associe au sample. | id | 0.0% | 32 |
| `process_software` | Version ou nom du logiciel de traitement. | texte | 0.0% | 2 |
| `process_date` | Date du traitement image. | date | 0.0% | 27 |
| `process_time` | Heure du traitement image. | heure | 0.0% | 32 |
| `process_first_img` | Premiere image traitee dans le profil ou sample. | index/image | 0.0% | 32 |
| `process_last_img` | Derniere image traitee dans le profil ou sample. | index/image | 0.0% | 2 |
| `process_pressure_gain` | Parametre de correction ou gain de pression utilise au traitement. | parametre | 0.0% | 2 |

## process/calibration

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `process_calibration` | Date ou identifiant de calibration UVP utilise au traitement. | texte | 0.0% | 2 |
| `process_pixel` | Dimension pixel utilisee au traitement. | mm | 0.0% | 2 |

## process/segmentation

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `process_upper` | Seuil superieur ou parametre de segmentation Zooprocess. | parametre | 0.0% | 2 |

## process/image

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `process_gamma` | Parametre gamma applique aux vignettes ou au traitement image. | parametre | 0.0% | 2 |

## process/filtre

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `process_esdmin` | ESD minimum retenu au traitement. | mm | 0.0% | 2 |
| `process_esdmax` | ESD maximum retenu au traitement. | mm | 0.0% | 2 |

## acquisition

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `acq_id` | Identifiant de l acquisition UVP5. | id | 0.0% | 32 |
| `acq_sn` | Numero de serie de l instrument UVP5. | texte | 0.0% | 2 |
| `acq_volimage` | Volume image par image. | L | 0.0% | 2 |

## acquisition/calibration

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `acq_aa` | Facteur de calibration Aa. | sans unite | 0.0% | 2 |
| `acq_exp` | Facteur de calibration Exp. | sans unite | 0.0% | 2 |
| `acq_pixel` | Dimension d un pixel dans le plan image. Necessaire pour convertir pixels en mm. | mm | 0.0% | 2 |

## classification

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `classif_id` | Identifiant EcoTaxa de la classe taxonomique valide. | id | 0.0% | 39 |

## classification/audit

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `classif_who` | Identifiant ou nom de l annotateur/classificateur. | texte | 0.0% | 15 |

## classification/auto

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `classif_auto_name` | Nom de la classe proposee par classification automatique. A comparer a l annotation valide. | texte | 0.0% | 26 |

## interne/ecotaxa

| Colonne | Definition | Unite | Nulls | Valeurs distinctes |
|---|---|---:|---:|---:|
| `objid` | Identifiant interne EcoTaxa de l objet. Utile pour tracer la source, pas pour l analyse scientifique. | id interne | 0.0% | 84668 |
| `processid_internal` | Identifiant interne EcoTaxa du process. | id interne | 0.0% | 32 |
| `acq_id_internal` | Identifiant interne EcoTaxa de l acquisition. | id interne | 0.0% | 32 |
| `sample_id_internal` | Identifiant interne EcoTaxa du sample. | id interne | 0.0% | 32 |
| `object_random_value` | Valeur interne aleatoire EcoTaxa, variable mais non scientifique. | sans unite | 0.0% | 84666 |
