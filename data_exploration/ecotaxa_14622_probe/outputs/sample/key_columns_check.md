# Verification des colonnes cles - EcoTaxa 14622

Verification basee sur la metadata projet EcoTaxa, sans export objet complet.

| Concept | Statut | Colonnes trouvees | Colonnes candidates cherchees |
|---|---|---|---|
| Identifiant objet | OK | `obj.orig_id` | `obj.orig_id` |
| Latitude objet | OK | `obj.latitude`, `sample.latitude` | `obj.latitude`, `sample.latitude` |
| Longitude objet | OK | `obj.longitude`, `sample.longitude` | `obj.longitude`, `sample.longitude` |
| Date objet | OK | `obj.objdate`, `sample.deployment_date_start`, `sample.deployment_datetime_start` | `obj.objdate`, `sample.deployment_date_start`, `sample.deployment_datetime_start` |
| Heure objet | OK | `obj.objtime`, `sample.deployment_time_start`, `sample.deployment_time_start_str` | `obj.objtime`, `sample.deployment_time_start`, `sample.deployment_time_start_str` |
| Profondeur objet min | OK | `obj.depth_min`, `fre.Depth min` | `obj.depth_min`, `fre.Depth min` |
| Profondeur objet max | OK | `obj.depth_max` | `obj.depth_max` |
| Taxon affiche / valide | OK | `txo.display_name`, `txo.name` | `txo.display_name`, `txo.name` |
| Statut de validation | OK | `obj.classif_qual` | `obj.classif_qual` |
| Classification automatique | OK | `obj.classif_auto_id`, `obj.classif_auto_score`, `obj.classif_auto_when` | `obj.classif_auto_id`, `obj.classif_auto_score`, `obj.classif_auto_when` |
| ESD / diametre equivalent | OK | `fre.equivalent_diameter_area` | `fre.equivalent_diameter_area` |
| Grand axe | OK | `fre.axis_major_length` | `fre.axis_major_length` |
| Petit axe | OK | `fre.axis_minor_length` | `fre.axis_minor_length` |
| Feret max | OK | `fre.feret_diameter_max` | `fre.feret_diameter_max` |
| Surface objet | OK | `fre.area`, `fre.area_filled`, `fre.area_convex` | `fre.area`, `fre.area_filled`, `fre.area_convex` |
| Intensite moyenne | OK | `fre.intensity_mean`, `fre.image_pixel_int_mean` | `fre.intensity_mean`, `fre.image_pixel_int_mean` |
| Calibration pixel | OK | `acq.pixel_um_size` | `acq.pixel_um_size` |
| Station | OK | `sample.station_name` | `sample.station_name` |
| Engin / filet | OK | `sample.gear`, `sample.gear_net_id`, `sample.net_mesh_size`, `sample.net_mouth_aperture` | `sample.gear`, `sample.gear_net_id`, `sample.net_mesh_size`, `sample.net_mouth_aperture` |
| CTD temperature | OK | `acq.temperature_ctd` | `acq.temperature_ctd` |
| CTD salinite | OK | `acq.salinity_ctd` | `acq.salinity_ctd` |
| CTD oxygene | OK | `acq.oxygen_concent`, `acq.oxygen_saturation` | `acq.oxygen_concent`, `acq.oxygen_saturation` |
| Fluorescence | OK | `acq.fluo1`, `acq.fluo2`, `acq.fluo3`, `acq.fluo4` | `acq.fluo1`, `acq.fluo2`, `acq.fluo3`, `acq.fluo4` |
| Profondeur acquisition | OK | `acq.raw_depth`, `acq.pressure_sensor_press` | `acq.raw_depth`, `acq.pressure_sensor_press` |

## Lecture rapide

- Les colonnes essentielles pour objet, temps, position, profondeur, taxonomie, taille et CTD sont presentes.
- La calibration est disponible via `acq.pixel_um_size` ; convertir les longueurs image en millimetres avec `pixel_um_size / 1000` si les mesures morphometriques sont en pixels.
- `txo.display_name` est le meilleur candidat pour le taxon affiche ; `obj.classif_qual` sert a verifier le statut de validation.
- Sans TSV objet, il ne faut pas supprimer de colonnes pour nullite ou constance : cette verification demande un export d'objets ou un echantillon exploitable.
