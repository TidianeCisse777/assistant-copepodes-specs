# OGSL probe sample

This folder contains a small real OGSL extract fetched from the public ERDDAP endpoint.

## Source

- Organization: Observatoire global du Saint-Laurent (OGSL)
- Dataset: `ismerSgdeCtd`
- Mission: `2024_06 BioDiv`
- File: `ogsl_ctd_biodiv_2024_sample.csv`

## Query used

```text
https://erddap.ogsl.ca/erddap/tabledap/ismerSgdeCtd.csv?cruiseID,cruise_start_date,cruise_end_date,cruise_chief_scientist,platform_name,instrument,stationID,cast_number,time,latitude,longitude,PRES,TE90,PSAL,ASAL,FLOR,OXYM,PSAR,SIGT,TRAN&cruiseID=%222024_06%20BioDiv%22&time>=2024-05-02T07:00:00Z
```

## Notes

- This is a CTD profile extract from the St. Lawrence Gulf context.
- The CSV preserves the ERDDAP-style units row so downstream tools can inspect the fields.
- The sample is intentionally small and contains a few rows only, to keep it lightweight for tests and probes.
