# TSV examples

Generated lightweight TSV examples from the validated probes.

## Files

- `loki_2331_ecotaxa_export_sample_50.tsv`: first 50 rows from the authenticated EcoTaxa LOKI project 2331 export.
- `uvp_amundsen_1165_ecotaxa_object_sample.tsv`: EcoTaxa 1165 object sample with UVP morphometry fields.
- `uvp_amundsen_1165_105_join_preview.tsv`: minimal join preview between EcoTaxa 1165 objects and EcoPart 105 profiles.
- `uvp_amundsen_105_ecopart_particles_reduced.tsv`: EcoPart CTD variables plus particle concentrations and biovolumes by profile/depth.
- `uvp_amundsen_1165_105_enriched_nearest_depth.tsv`: object-level test table enriched with nearest EcoPart depth row.
- `amundsen_12713_ctd_2018_sample.tsv`: Amundsen Science CTD ERDDAP sample for 2018.
- `amundsen_12713_ctd_ips007_match_sample.tsv`: official Amundsen CTD cast matching EcoPart profile `ips_007`.
- `uvp_amundsen_105_ecopart_vs_amundsen_ctd_compare.tsv`: nearest-depth comparison between EcoPart `ips_007` and official Amundsen CTD.

## Row counts

- LOKI sample rows: 50
- UVP EcoTaxa object sample rows: 25
- Join preview rows: 25
- EcoPart particle reduced sample rows: 50
- Enriched nearest-depth rows: 25
- Amundsen CTD sample rows: 50
- Amundsen CTD `ips_007` match rows: 1004
- EcoPart vs Amundsen comparison rows: 50

The original full LOKI TSV was validated during the probe, then removed from the cleaned repo. Regenerate it with:

```bash
cd ../ecotaxa_loki_probe
python src/export_loki_authenticated.py
```
