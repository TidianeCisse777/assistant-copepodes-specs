Minimal join test — EcoTaxa 1165 + EcoPart 105

1. Objets EcoTaxa testes : 25
2. Objets relies a un profile_id EcoPart : 25/25
3. Profils EcoPart disponibles : 7
4. Dates concordantes : 25/25
5. Delta lat max : 0.0002666666667039408
6. Delta lon max : 0.00010000000000331966
7. Cle utilisee :
   - extraire profile_id depuis EcoTaxa obj_orig_id, ex. ips_007_899 -> ips_007
   - joindre avec EcoPart profile_id issu de getsamplepopover
8. Colonnes ajoutees cote EcoPart :
   - ecopart_sample_id
   - ecopart_lat / ecopart_lon
   - ecopart_date / ecopart_time
   - ship / cruise / ecopart_project / ecotaxa_project
9. Conclusion :
   - jointure structurelle valide ? oui
   - prochaine etape : obtenir/exporter les tables EcoPart CTD/particules pour joindre par profile_id + profondeur

Extrait de jointure conserve : ../examples_tsv/uvp_amundsen_1165_105_join_preview.tsv
