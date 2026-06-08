# NeoLabs per-stage taxonomy enriched with Amundsen CTD

- Output TSV: `examples_tsv/neolabs_taxonomy_stages_amundsen_ctd.tsv`
- Rows written: 5047
- Unique sample/analysis contexts in output: 396
- Unique sample/analysis contexts checked against Amundsen: 387
- Abundance source: `Donnée Neolabs Taxon/IDEA Taxonomy Samples and Analyses Data Metadata May 26 2026.csv`
- Sample metadata source: `Donnée Neolabs Taxon/donne_sample.csv`
- Amundsen CTD source: `https://erddap.amundsenscience.com/erddap/tabledap/amundsen12713.csvp`

CTD match statuses by context:

- `matched`: 236
- `outside_amundsen_ctd_range`: 135
- `no_match_72h_1.00deg`: 16
- `missing_sample_metadata`: 9

CTD match statuses by row:

- `matched`: 3038
- `outside_amundsen_ctd_range`: 1679
- `no_match_72h_1.00deg`: 224
- `missing_sample_metadata`: 106

Join logic:

- NeoLabs per-stage abundances are joined to `donne_sample.csv` on `SAMPLE_ID` + `ANALYSIS_ID`.
- ERDDAP CTD candidates are queried by deployment datetime and sample latitude/longitude.
- The best CTD cast is selected by time delta, horizontal distance, and sampled-depth coverage.
- CTD values are attached as nearest-mid-depth values plus mean/min/max over the sampled depth interval.
- Samples outside the official Amundsen CTD time range are retained with `ctd_match_status=outside_amundsen_ctd_range`.
