# EcoTaxa 1165 + EcoPart 105 depth-enriched table

- Objets EcoTaxa: 25
- Objets enrichis avec EcoPart: 25/25
- Methode: `profile_id + profondeur EcoPart la plus proche`
- Delta profondeur median: 59.600 m
- Delta profondeur max: 693.400 m
- Qualite des matchs profondeur: {'outside_ecopart_sample_range': 16, 'within_5m_bin': 9}
- Sortie TSV: `examples_tsv/uvp_amundsen_1165_105_enriched_nearest_depth.tsv`

Colonnes ajoutees depuis EcoPart:

- `ecopart_depth`
- `depth_delta_m`
- `depth_match_quality`
- `ecopart_temperature_degC`
- `ecopart_salinity_psu`
- `ecopart_oxygen_umol_kg` / `ecopart_oxygen_ml_l`
- `ecopart_fluorescence_mg_chl_m3`
- `ecopart_nitrate_umol_l`
- `ecopart_particle_count_l_selected_sum`
- `ecopart_particle_biovolume_selected_sum`

Limite: ce test utilise les extraits TSV conserves, pas les exports complets. Les lignes `outside_ecopart_sample_range` indiquent que l'objet est plus profond que l'extrait EcoPart disponible.
