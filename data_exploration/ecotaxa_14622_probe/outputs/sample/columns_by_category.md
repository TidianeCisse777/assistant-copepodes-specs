# Colonnes EcoTaxa LOKI - ArcticNet 2015

Projet EcoTaxa `14622`. Extraction metadata-only, sans telechargement des objets.
Total : 281 colonnes detectees dans la metadata projet.

Note : ce rapport classe les colonnes disponibles. Il ne prouve pas quelles colonnes sont nulles ou constantes dans les objets, car aucun TSV objet complet n'a ete exporte.

## 1. Identification, position, temps et profondeur de l'objet

- `obj.orig_id` - Identifiant original de l'objet
- `obj.latitude` - Latitude de l'objet
- `obj.longitude` - Longitude de l'objet
- `obj.objdate` - Date de l'objet
- `obj.objtime` - Heure de l'objet
- `obj.depth_min` - Profondeur minimale
- `obj.depth_max` - Profondeur maximale

## 2. Taxonomie, validation et classification automatique

- `obj.classif_qual` - Statut de classification
- `obj.classif_id` - Identifiant taxonomique retenu
- `obj.classif_who` - Validateur ou classificateur
- `obj.classif_when` - Date de classification
- `obj.classif_auto_id` - Identifiant taxonomique automatique
- `obj.classif_auto_score` - Score de classification automatique
- `obj.classif_auto_when` - Date de classification automatique
- `txo.display_name` - Nom taxonomique affiche
- `txo.name` - Nom taxonomique brut
- `txo.id` - Identifiant taxonomique EcoTaxa
- `txo.parent_id` - Identifiant du parent taxonomique
- `txo.aphia_id` - Identifiant Aphia/WoRMS si disponible

## 3. Colonnes affichees dans l'interface de classification

- `fre.equivalent_diameter_area` - ESD
- `fre.axis_major_length` - Major
- `fre.axis_minor_length` - Minor
- `fre.Depth min` - Depth

## 4. Morphometrie - taille et surface

- `fre.area` (n14) - area
- `fre.area_bbox` (n15) - area bbox
- `fre.area_convex` (n16) - area convex
- `fre.area_filled` (n17) - area filled
- `fre.axis_major_length` (n18) - axis major length
- `fre.axis_minor_length` (n19) - axis minor length
- `fre.equivalent_diameter_area` (n33) - equivalent diameter area
- `fre.feret_diameter_max` (n36) - feret diameter max

## 5. Morphometrie - forme, contour et position image

- `fre.orientation` (n151) - orientation
- `fre.perimeter` (n152) - perimeter
- `fre.perimeter_crofton` (n153) - perimeter crofton
- `fre.solidity` (n154) - solidity
- `fre.trimmed_masked_image_numb_of_regions` (n156) - trimmed masked image numb of regions
- `fre.trimmed_mask_numb_of_regions` (n157) - trimmed mask numb of regions
- `fre.trimmed_labeled_mask_numb_of_regions` (n158) - trimmed labeled mask numb of regions
- `fre.bbox-0` (n20) - bbox-0
- `fre.bbox-1` (n21) - bbox-1
- `fre.bbox-2` (n22) - bbox-2
- `fre.bbox-3` (n23) - bbox-3
- `fre.centroid-0` (n24) - centroid-0
- `fre.centroid-1` (n25) - centroid-1
- `fre.centroid_local-0` (n26) - centroid local-0
- `fre.centroid_local-1` (n27) - centroid local-1
- `fre.centroid_weighted-0` (n28) - centroid weighted-0
- `fre.centroid_weighted-1` (n29) - centroid weighted-1
- `fre.centroid_weighted_local-0` (n30) - centroid weighted local-0
- `fre.centroid_weighted_local-1` (n31) - centroid weighted local-1
- `fre.eccentricity` (n32) - eccentricity
- `fre.euler_number` (n34) - euler number
- `fre.extent` (n35) - extent
- `fre.inertia_tensor-0-0` (n37) - inertia tensor-0-0
- `fre.inertia_tensor-0-1` (n38) - inertia tensor-0-1
- `fre.inertia_tensor-1-0` (n39) - inertia tensor-1-0
- `fre.inertia_tensor-1-1` (n40) - inertia tensor-1-1
- `fre.inertia_tensor_eigvals-0` (n41) - inertia tensor eigvals-0
- `fre.inertia_tensor_eigvals-1` (n42) - inertia tensor eigvals-1

## 6. Intensite, niveaux de gris et texture

- `fre.image_pixel_low_extrema` (n08) - image pixel low extrema
- `fre.image_pixel_high_extrema` (n09) - image pixel high extrema
- `fre.image_pixel_count` (n10) - image pixel count
- `fre.image_pixel_int_mean` (n11) - image pixel int mean
- `fre.image_pixel_int_variance` (n12) - image pixel int variance
- `fre.image_pixel_int_stddev` (n13) - image pixel int stddev
- `fre.threshold` (n155) - threshold
- `fre.intensity_max` (n43) - intensity max
- `fre.intensity_mean` (n44) - intensity mean
- `fre.intensity_min` (n45) - intensity min

## 7. Moments mathematiques et descripteurs derives

- `fre.moments_weighted-0-1` (n100) - moments weighted-0-1
- `fre.moments_weighted-0-2` (n101) - moments weighted-0-2
- `fre.moments_weighted-0-3` (n102) - moments weighted-0-3
- `fre.moments_weighted-1-0` (n103) - moments weighted-1-0
- `fre.moments_weighted-1-1` (n104) - moments weighted-1-1
- `fre.moments_weighted-1-2` (n105) - moments weighted-1-2
- `fre.moments_weighted-1-3` (n106) - moments weighted-1-3
- `fre.moments_weighted-2-0` (n107) - moments weighted-2-0
- `fre.moments_weighted-2-1` (n108) - moments weighted-2-1
- `fre.moments_weighted-2-2` (n109) - moments weighted-2-2
- `fre.moments_weighted-2-3` (n110) - moments weighted-2-3
- `fre.moments_weighted-3-0` (n111) - moments weighted-3-0
- `fre.moments_weighted-3-1` (n112) - moments weighted-3-1
- `fre.moments_weighted-3-2` (n113) - moments weighted-3-2
- `fre.moments_weighted-3-3` (n114) - moments weighted-3-3
- `fre.moments_weighted_central-0-0` (n115) - moments weighted central-0-0
- `fre.moments_weighted_central-0-1` (n116) - moments weighted central-0-1
- `fre.moments_weighted_central-0-2` (n117) - moments weighted central-0-2
- `fre.moments_weighted_central-0-3` (n118) - moments weighted central-0-3
- `fre.moments_weighted_central-1-0` (n119) - moments weighted central-1-0
- `fre.moments_weighted_central-1-1` (n120) - moments weighted central-1-1
- `fre.moments_weighted_central-1-2` (n121) - moments weighted central-1-2
- `fre.moments_weighted_central-1-3` (n122) - moments weighted central-1-3
- `fre.moments_weighted_central-2-0` (n123) - moments weighted central-2-0
- `fre.moments_weighted_central-2-1` (n124) - moments weighted central-2-1
- `fre.moments_weighted_central-2-2` (n125) - moments weighted central-2-2
- `fre.moments_weighted_central-2-3` (n126) - moments weighted central-2-3
- `fre.moments_weighted_central-3-0` (n127) - moments weighted central-3-0
- `fre.moments_weighted_central-3-1` (n128) - moments weighted central-3-1
- `fre.moments_weighted_central-3-2` (n129) - moments weighted central-3-2
- `fre.moments_weighted_central-3-3` (n130) - moments weighted central-3-3
- `fre.moments_weighted_hu-0` (n131) - moments weighted hu-0
- `fre.moments_weighted_hu-1` (n132) - moments weighted hu-1
- `fre.moments_weighted_hu-2` (n133) - moments weighted hu-2
- `fre.moments_weighted_hu-3` (n134) - moments weighted hu-3
- `fre.moments_weighted_hu-4` (n135) - moments weighted hu-4
- `fre.moments_weighted_hu-5` (n136) - moments weighted hu-5
- `fre.moments_weighted_hu-6` (n137) - moments weighted hu-6
- `fre.moments_weighted_normalized-0-2` (n138) - moments weighted normalized-0-2
- `fre.moments_weighted_normalized-0-3` (n139) - moments weighted normalized-0-3
- `fre.moments_weighted_normalized-1-1` (n140) - moments weighted normalized-1-1
- `fre.moments_weighted_normalized-1-2` (n141) - moments weighted normalized-1-2
- `fre.moments_weighted_normalized-1-3` (n142) - moments weighted normalized-1-3
- `fre.moments_weighted_normalized-2-0` (n143) - moments weighted normalized-2-0
- `fre.moments_weighted_normalized-2-1` (n144) - moments weighted normalized-2-1
- `fre.moments_weighted_normalized-2-2` (n145) - moments weighted normalized-2-2
- `fre.moments_weighted_normalized-2-3` (n146) - moments weighted normalized-2-3
- `fre.moments_weighted_normalized-3-0` (n147) - moments weighted normalized-3-0
- `fre.moments_weighted_normalized-3-1` (n148) - moments weighted normalized-3-1
- `fre.moments_weighted_normalized-3-2` (n149) - moments weighted normalized-3-2
- `fre.moments_weighted_normalized-3-3` (n150) - moments weighted normalized-3-3
- `fre.log_moments_central-0-1` (n159) - log moments central-0-1
- `fre.log_moments_central-1-0` (n160) - log moments central-1-0
- `fre.log_moments_hu-1` (n161) - log moments hu-1
- `fre.log_moments_hu-2` (n162) - log moments hu-2
- `fre.log_moments_hu-3` (n163) - log moments hu-3
- `fre.log_moments_hu-4` (n164) - log moments hu-4
- `fre.log_moments_hu-5` (n165) - log moments hu-5
- `fre.log_moments_hu-6` (n166) - log moments hu-6
- `fre.log_moments_normalized-0-3` (n167) - log moments normalized-0-3
- `fre.log_moments_normalized-1-1` (n168) - log moments normalized-1-1
- `fre.log_moments_normalized-1-2` (n169) - log moments normalized-1-2
- `fre.log_moments_normalized-1-3` (n170) - log moments normalized-1-3
- `fre.log_moments_normalized-2-1` (n171) - log moments normalized-2-1
- `fre.log_moments_normalized-2-2` (n172) - log moments normalized-2-2
- `fre.log_moments_normalized-2-3` (n173) - log moments normalized-2-3
- `fre.log_moments_normalized-3-0` (n174) - log moments normalized-3-0
- `fre.log_moments_normalized-3-1` (n175) - log moments normalized-3-1
- `fre.log_moments_normalized-3-2` (n176) - log moments normalized-3-2
- `fre.log_moments_normalized-3-3` (n177) - log moments normalized-3-3
- `fre.log_moments_weighted_central-0-1` (n178) - log moments weighted central-0-1
- `fre.log_moments_weighted_central-1-0` (n179) - log moments weighted central-1-0
- `fre.log_moments_weighted_hu-0` (n180) - log moments weighted hu-0
- `fre.log_moments_weighted_hu-1` (n181) - log moments weighted hu-1
- `fre.log_moments_weighted_hu-2` (n182) - log moments weighted hu-2
- `fre.log_moments_weighted_hu-3` (n183) - log moments weighted hu-3
- `fre.log_moments_weighted_hu-4` (n184) - log moments weighted hu-4
- `fre.log_moments_weighted_hu-5` (n185) - log moments weighted hu-5
- `fre.log_moments_weighted_hu-6` (n186) - log moments weighted hu-6
- `fre.log_moments_weighted_normalized-0-2` (n187) - log moments weighted normalized-0-2
- `fre.log_moments_weighted_normalized-0-3` (n188) - log moments weighted normalized-0-3
- `fre.log_moments_weighted_normalized-1-1` (n189) - log moments weighted normalized-1-1
- `fre.log_moments_weighted_normalized-1-2` (n190) - log moments weighted normalized-1-2
- `fre.log_moments_weighted_normalized-1-3` (n191) - log moments weighted normalized-1-3
- `fre.log_moments_weighted_normalized-2-0` (n192) - log moments weighted normalized-2-0
- `fre.log_moments_weighted_normalized-2-1` (n193) - log moments weighted normalized-2-1
- `fre.log_moments_weighted_normalized-2-2` (n194) - log moments weighted normalized-2-2
- `fre.log_moments_weighted_normalized-2-3` (n195) - log moments weighted normalized-2-3
- `fre.log_moments_weighted_normalized-3-0` (n196) - log moments weighted normalized-3-0
- `fre.log_moments_weighted_normalized-3-1` (n197) - log moments weighted normalized-3-1
- `fre.log_moments_weighted_normalized-3-2` (n198) - log moments weighted normalized-3-2
- `fre.log_moments_weighted_normalized-3-3` (n199) - log moments weighted normalized-3-3
- `fre.moments-0-0` (n47) - moments-0-0
- `fre.moments-0-1` (n48) - moments-0-1
- `fre.moments-0-2` (n49) - moments-0-2
- `fre.moments-0-3` (n50) - moments-0-3
- `fre.moments-1-0` (n51) - moments-1-0
- `fre.moments-1-1` (n52) - moments-1-1
- `fre.moments-1-2` (n53) - moments-1-2
- `fre.moments-1-3` (n54) - moments-1-3
- `fre.moments-2-0` (n55) - moments-2-0
- `fre.moments-2-1` (n56) - moments-2-1
- `fre.moments-2-2` (n57) - moments-2-2
- `fre.moments-2-3` (n58) - moments-2-3
- `fre.moments-3-0` (n59) - moments-3-0
- `fre.moments-3-1` (n60) - moments-3-1
- `fre.moments-3-2` (n61) - moments-3-2
- `fre.moments-3-3` (n62) - moments-3-3
- `fre.moments_central-0-0` (n63) - moments central-0-0
- `fre.moments_central-0-1` (n64) - moments central-0-1
- `fre.moments_central-0-2` (n65) - moments central-0-2
- `fre.moments_central-0-3` (n66) - moments central-0-3
- `fre.moments_central-1-0` (n67) - moments central-1-0
- `fre.moments_central-1-1` (n68) - moments central-1-1
- `fre.moments_central-1-2` (n69) - moments central-1-2
- `fre.moments_central-1-3` (n70) - moments central-1-3
- `fre.moments_central-2-0` (n71) - moments central-2-0
- `fre.moments_central-2-1` (n72) - moments central-2-1
- `fre.moments_central-2-2` (n73) - moments central-2-2
- `fre.moments_central-2-3` (n74) - moments central-2-3
- `fre.moments_central-3-0` (n75) - moments central-3-0
- `fre.moments_central-3-1` (n76) - moments central-3-1
- `fre.moments_central-3-2` (n77) - moments central-3-2
- `fre.moments_central-3-3` (n78) - moments central-3-3
- `fre.moments_hu-0` (n79) - moments hu-0
- `fre.moments_hu-1` (n80) - moments hu-1
- `fre.moments_hu-2` (n81) - moments hu-2
- `fre.moments_hu-3` (n82) - moments hu-3
- `fre.moments_hu-4` (n83) - moments hu-4
- `fre.moments_hu-5` (n84) - moments hu-5
- `fre.moments_hu-6` (n85) - moments hu-6
- `fre.moments_normalized-0-2` (n86) - moments normalized-0-2
- `fre.moments_normalized-0-3` (n87) - moments normalized-0-3
- `fre.moments_normalized-1-1` (n88) - moments normalized-1-1
- `fre.moments_normalized-1-2` (n89) - moments normalized-1-2
- `fre.moments_normalized-1-3` (n90) - moments normalized-1-3
- `fre.moments_normalized-2-0` (n91) - moments normalized-2-0
- `fre.moments_normalized-2-1` (n92) - moments normalized-2-1
- `fre.moments_normalized-2-2` (n93) - moments normalized-2-2
- `fre.moments_normalized-2-3` (n94) - moments normalized-2-3
- `fre.moments_normalized-3-0` (n95) - moments normalized-3-0
- `fre.moments_normalized-3-1` (n96) - moments normalized-3-1
- `fre.moments_normalized-3-2` (n97) - moments normalized-3-2
- `fre.moments_normalized-3-3` (n98) - moments normalized-3-3
- `fre.moments_weighted-0-0` (n99) - moments weighted-0-0

## 8. Detection, vignette et doublons

- `fre.frame_ms` (n01) - frame ms
- `fre.frame_vignette_number` (n02) - frame vignette number
- `fre.vignette_x_pos` (n03) - vignette x pos
- `fre.vignette_y_pos` (n04) - vignette y pos
- `fre.orig_img_bmp_file_size` (n05) - orig img bmp file size
- `fre.image_height` (n06) - image height
- `fre.image_width` (n07) - image width
- `fre.double_position` (n200) - double position
- `fre.total_doubles` (n201) - total doubles
- `fre.label_id_number` (n46) - label id number
- `fre.double_prediction` (t01) - double prediction
- `fre.double_validation_status` (t02) - double validation status
- `fre.double_probability` (t03) - double probability
- `fre.double_of` (t04) - double of

## 9. Sample, station et deploiement

- `sample.station_name` (t01) - station name
- `sample.deployment_date_start` (t02) - deployment date start
- `sample.deployment_time_start` (t03) - deployment time start
- `sample.deployment_datetime_end` (t04) - deployment datetime end
- `sample.gear` (t05) - gear
- `sample.tow_type` (t06) - tow type
- `sample.cast_number` (t07) - cast number
- `sample.bottom_depth` (t08) - bottom depth
- `sample.latitude` (t09) - latitude
- `sample.longitude` (t10) - longitude
- `sample.deployment_comments` (t11) - deployment comments
- `sample.gear_net_id` (t12) - gear net id
- `sample.net_mesh_size` (t13) - net mesh size
- `sample.net_mouth_aperture` (t14) - net mouth aperture
- `sample.max_net_sampling_depth` (t15) - max net sampling depth
- `sample.min_net_sampling_depth` (t16) - min net sampling depth
- `sample.deployment_datetime_start` (t17) - deployment datetime start
- `sample.deployment_time_start_str` (t18) - deployment time start str

## 10. Acquisition LOKI, CTD embarquee et capteurs

- `acq.original_telemetry_profil_folder` (t01) - original telemetry profil folder
- `acq.vprm version` (t02) - vprm version
- `acq.sound_velocity` (t03) - sound velocity
- `acq.density_ctd` (t04) - density ctd
- `acq.temperature_ctd` (t05) - temperature ctd
- `acq.conductivity_ctd` (t06) - conductivity ctd
- `acq.salinity_ctd` (t07) - salinity ctd
- `acq.oxygen_concent` (t08) - oxygen concent
- `acq.oxygen_saturation` (t09) - oxygen saturation
- `acq.oxygen_temperature` (t10) - oxygen temperature
- `acq.loki_temperature` (t11) - loki temperature
- `acq.loki_voltage` (t12) - loki voltage
- `acq.status_acquire` (t13) - status acquire
- `acq.speed` (t14) - speed
- `acq.pitch` (t15) - pitch
- `acq.roll` (t16) - roll
- `acq.fluo1` (t17) - fluo1
- `acq.fluo2` (t18) - fluo2
- `acq.fluo3` (t19) - fluo3
- `acq.fluo4` (t20) - fluo4
- `acq.pressure_sensor_press` (t21) - pressure sensor press
- `acq.pressure_sensor_temp` (t22) - pressure sensor temp
- `acq.camera_status` (t23) - camera status
- `acq.vprcl_status` (t24) - vprcl status
- `acq.vprcl_picture_number` (t25) - vprcl picture number
- `acq.vprcl_framerate` (t26) - vprcl framerate
- `acq.raw_depth` (t27) - raw depth
- `acq.depth_outlier` (t28) - depth outlier
- `acq.pixel_um_size` (t29) - pixel um size

## 11. Process / traitement image

- `process.footer_height_px` (t01) - footer height px
- `process.python_img_feats_library` (t02) - python img feats library

## 12. Colonnes internes ou peu analytiques

- `obj.complement_info` - Information complementaire objet
- `obj.object_link` - Lien objet
- `obj.random_value` - Valeur aleatoire interne
- `obj.sunpos` - Position solaire calculee

## Colonnes prioritaires pour analyses copepodes

- Spatio-temporel : `obj.latitude`, `obj.longitude`, `obj.objdate`, `obj.objtime`
- Profondeur : `obj.depth_min`, `obj.depth_max`, `fre.Depth min`, `acq.raw_depth`
- Taxon valide : `txo.display_name`, `txo.name`, `obj.classif_qual`
- Taille : `fre.equivalent_diameter_area`, `fre.axis_major_length`, `fre.axis_minor_length`, `fre.feret_diameter_max`, `fre.area`
- Forme : `fre.eccentricity`, `fre.extent`, `fre.solidity`, `fre.perimeter`, `fre.orientation`
- Intensite : `fre.intensity_mean`, `fre.intensity_min`, `fre.intensity_max`, `fre.image_pixel_int_mean`, `fre.image_pixel_int_stddev`
- Sample/deploiement : `sample.station_name`, `sample.deployment_datetime_start`, `sample.gear`, `sample.tow_type`, `sample.cast_number`
- Filet : `sample.net_mesh_size`, `sample.net_mouth_aperture`, `sample.min_net_sampling_depth`, `sample.max_net_sampling_depth`
- CTD/capteurs : `acq.temperature_ctd`, `acq.salinity_ctd`, `acq.oxygen_concent`, `acq.fluo1`, `acq.raw_depth`, `acq.pixel_um_size`
