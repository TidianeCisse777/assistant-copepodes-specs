# NeoLabs taxonomy abundances enriched with Amundsen CTD

- Output TSV: `examples_tsv/neolabs_taxonomy_abundance_amundsen_ctd.tsv`
- Rows written: 11378
- Unique sample/analysis contexts in output: 421
- Unique sample/analysis contexts checked against Amundsen: 412
- Abundance source: `Donnée Neolabs Taxon/IDEA Taxonomy Zooplankton Abundances Data May 26 2026.csv`
- Sample metadata source: `Donnée Neolabs Taxon/donne_sample.csv`
- Amundsen CTD source: `https://erddap.amundsenscience.com/erddap/tabledap/amundsen12713.csvp`

CTD match statuses by context:

- `matched`: 261
- `outside_amundsen_ctd_range`: 135
- `no_match_72h_1.00deg`: 16
- `missing_sample_metadata`: 9

CTD match statuses by row:

- `matched`: 6840
- `outside_amundsen_ctd_range`: 3615
- `no_match_72h_1.00deg`: 562
- `missing_sample_metadata`: 361

Join logic:

- NeoLabs abundances are joined to `donne_sample.csv` on `SAMPLE_ID` + `ANALYSIS_ID`.
- ERDDAP CTD candidates are queried by deployment datetime and sample latitude/longitude.
- The best CTD cast is selected by time delta, horizontal distance, and sampled-depth coverage.
- CTD values are attached as nearest-mid-depth values plus mean/min/max over the sampled depth interval.
- Samples outside the official Amundsen CTD time range are retained with `ctd_match_status=outside_amundsen_ctd_range`.
