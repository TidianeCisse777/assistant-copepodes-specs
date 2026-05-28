# Bio-ORACLE probe sample

This folder contains a small real Bio-ORACLE extract fetched from the official ERDDAP endpoint.

## Source

- Dataset: `si_ssp126_2020_2100_depthmean`
- Variable: `si_mean`
- File: `bio_oracle_si_mean_ssp126_2020_sample.csv`

## Query used

```text
https://erddap.bio-oracle.org/erddap/griddap/si_ssp126_2020_2100_depthmean.csv?si_mean[(2020-01-01T00:00:00Z)][(lat)][(lon)]
```

The sample rows were pulled at a few oceanic coordinates to avoid land-only `NaN` values.

## Notes

- Bio-ORACLE is a gridded environmental dataset, not a tabular observational export.
- The CSV keeps the ERDDAP-style header and units row so downstream tooling can inspect the format.
