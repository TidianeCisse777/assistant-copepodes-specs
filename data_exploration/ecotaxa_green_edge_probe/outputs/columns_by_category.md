# Colonnes EcoTaxa UVP5 GREEN EDGE Ice Camp 2015

Export EcoTaxa projet 42. Total : 161 colonnes.

## 1. Identification, position, temps et profondeur de l'objet

- `object_id`
- `object_lat`
- `object_lon`
- `object_date`
- `object_time`
- `object_link`
- `object_depth_min`
- `object_depth_max`
- `object_random_value`
- `object_sunpos`

## 2. Annotation humaine / statut de validation

- `object_annotation_status`
- `object_annotation_person_name`
- `object_annotation_person_email`
- `object_annotation_date`
- `object_annotation_time`
- `object_annotation_category`
- `object_annotation_hierarchy`

## 3. Taxonomie / classification automatique

- `classif_id`
- `classif_who`
- `classif_auto_id`
- `classif_auto_name`
- `classif_auto_score`
- `classif_auto_when`

## 4. Informations complementaires

- `complement_info`
- `object_tag`

## 5. Morphometrie geometrique de l'objet

- `object_area`
- `object_x`
- `object_y`
- `object_xm`
- `object_ym`
- `object_perim.`
- `object_bx`
- `object_by`
- `object_width`
- `object_height`
- `object_major`
- `object_minor`
- `object_angle`
- `object_circ.`
- `object_feret`
- `object_%area`
- `object_xstart`
- `object_ystart`
- `object_area_exc`
- `object_fractal`
- `object_skelarea`
- `object_convperim`
- `object_convarea`
- `object_thickr`
- `object_areai`
- `object_esd`
- `object_elongation`
- `object_centroids`
- `object_perimareaexc`
- `object_feretareaexc`
- `object_perimferet`
- `object_perimmajor`
- `object_circex`
- `object_cdexc`
- `object_convperim_perim`
- `object_convarea_area`
- `object_skeleton_area`

## 6. Intensite, niveaux de gris et texture

- `object_mean`
- `object_stddev`
- `object_mode`
- `object_min`
- `object_max`
- `object_intden`
- `object_median`
- `object_skew`
- `object_kurt`
- `object_slope`
- `object_histcum1`
- `object_histcum2`
- `object_histcum3`
- `object_xmg5`
- `object_ymg5`
- `object_nb1`
- `object_nb2`
- `object_nb3`
- `object_compentropy`
- `object_compmean`
- `object_compslope`
- `object_compm1`
- `object_compm2`
- `object_compm3`
- `object_fcons`
- `object_range`
- `object_meanpos`
- `object_cv`
- `object_sr`
- `object_kurt_mean`
- `object_skew_mean`
- `object_nb1_area`
- `object_nb2_area`
- `object_nb3_area`
- `object_nb1_range`
- `object_nb2_range`
- `object_nb3_range`
- `object_median_mean`
- `object_median_mean_range`

## 7. Symetrie et ratios derives

- `object_symetrieh`
- `object_symetriev`
- `object_symetriehc`
- `object_symetrievc`
- `object_symetrieh_area`
- `object_symetriev_area`

## 8. Sample / profil terrain

- `sample_id`
- `sample_dataportal_descriptor`
- `sample_profileid`
- `sample_cruise`
- `sample_ship`
- `sample_stationid`
- `sample_bottomdepth`
- `sample_ctdrosettefilename`
- `sample_dn`
- `sample_winddir`
- `sample_windspeed`
- `sample_seastate`
- `sample_nebuloussness`
- `sample_yoyo`
- `sample_comment`
- `sample_barcode`
- `sample_lat`
- `sample_long`

## 9. Traitement image / process

- `process_id`
- `process_software`
- `process_date`
- `process_time`
- `process_first_img`
- `process_last_img`
- `process_pressure_gain`
- `process_calibration`
- `process_pixel`
- `process_upper`
- `process_gamma`
- `process_esdmin`
- `process_esdmax`

## 10. Acquisition UVP5

- `acq_id`
- `acq_instrument`
- `acq_sn`
- `acq_volimage`
- `acq_aa`
- `acq_exp`
- `acq_pixel`
- `acq_file_description`
- `acq_tasktype`
- `acq_disktype`
- `acq_shutterspeed`
- `acq_gain`
- `acq_threshold`
- `acq_smbase`
- `acq_smzoo`
- `acq_erase_border_blob`
- `acq_choice`
- `acq_ratio`
- `acq_exposure`

## 11. Identifiants internes EcoTaxa

- `objid`
- `processid_internal`
- `acq_id_internal`
- `sample_id_internal`

## Colonnes prioritaires pour analyses copépodes

- Spatio-temporel : `object_lat`, `object_lon`, `object_date`, `object_time`
- Profondeur : `object_depth_min`, `object_depth_max`
- Taxon valide : `object_annotation_category`, `object_annotation_hierarchy`, `object_annotation_status`
- Taille : `object_area`, `object_esd`, `object_major`, `object_minor`, `object_feret`
- Forme : `object_elongation`, `object_circ.`, `object_fractal`
- Profil/sample : `sample_profileid`, `sample_stationid`, `sample_cruise`
- Instrument : `acq_instrument`, `acq_sn`, `acq_volimage`
