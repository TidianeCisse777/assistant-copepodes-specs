# EcoPart 105 vs Amundsen official CTD

- Profile EcoPart teste: `ips_007`
- Temps EcoPart: 2018-07-16 13:54
- Cast Amundsen trouve: `7` station `1`
- Temps Amundsen: 2018-07-16T13:57:04Z
- Delta temps: 3.07 minutes
- Delta latitude: 0.000200
- Delta longitude: 0.000100
- Lignes CTD Amundsen recuperees: 1004
- Lignes EcoPart comparees: 50
- Delta profondeur median: 0.227 m
- Delta profondeur max: 0.484 m

Fichiers generes:

- `examples_tsv/amundsen_12713_ctd_ips007_match_sample.tsv`
- `examples_tsv/uvp_amundsen_105_ecopart_vs_amundsen_ctd_compare.tsv`

Conclusion:

- Le cast CTD officiel Amundsen correspondant au profil EcoPart existe dans ERDDAP.
- La comparaison directe est possible via date/time + lat/lon + profondeur proche.
- Ce test reste leger : il compare seulement le profil `ips_007` conserve dans les extraits.
