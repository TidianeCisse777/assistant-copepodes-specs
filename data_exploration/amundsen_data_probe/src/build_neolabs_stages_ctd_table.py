from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import timedelta
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np
import requests


ROOT = Path(__file__).resolve().parents[2]
NEOLABS = ROOT / "Donnée Neolabs Taxon"
EXAMPLES = ROOT / "examples_tsv"
RAW = ROOT / "amundsen_data_probe" / "outputs" / "raw" / "neolabs_ctd"
REPORT = ROOT / "amundsen_data_probe" / "outputs" / "report_neolabs_stages_ctd.md"

ABUNDANCE_PATH = NEOLABS / "IDEA Taxonomy Samples and Analyses Data Metadata May 26 2026.csv"
SAMPLE_METADATA_PATH = NEOLABS / "donne_sample.csv"
OUT = EXAMPLES / "neolabs_taxonomy_stages_amundsen_ctd.tsv"

ERDDAP_URL = "https://erddap.amundsenscience.com/erddap/tabledap/amundsen12713.csvp"
ERDDAP_VARIABLES = [
    "platform_name",
    "filename",
    "cruise_name",
    "cruise_number",
    "cast_number",
    "station",
    "time",
    "latitude",
    "longitude",
    "PRES",
    "depth",
    "TE90",
    "PSAL",
    "OXYM",
    "FLOR",
    "NTRA",
]

CTD_RANGE_START = pd.Timestamp("2014-07-15T08:20:04Z")
CTD_RANGE_END = pd.Timestamp("2024-10-01T02:03:25Z")

QUERY_ATTEMPTS = [
    {"hours": 12, "margin_deg": 0.30, "label": "12h_0.30deg"},
    {"hours": 24, "margin_deg": 0.50, "label": "24h_0.50deg"},
    {"hours": 72, "margin_deg": 1.00, "label": "72h_1.00deg"},
]

CTD_RENAME = {
    "time (UTC)": "amundsen_time",
    "latitude (degrees_north)": "amundsen_lat",
    "longitude (degrees_east)": "amundsen_lon",
    "PRES (decibars)": "amundsen_pres_db",
    "depth (m)": "amundsen_depth_m",
    "TE90 (degC)": "amundsen_temperature_degC",
    "PSAL (PSU)": "amundsen_salinity_psu",
    "OXYM (uM)": "amundsen_oxygen_uM",
    "FLOR (ug/L)": "amundsen_fluorescence_ug_l",
    "NTRA (mmol/m^3)": "amundsen_nitrate_mmol_m3",
}

CTD_VALUE_COLUMNS = [
    "amundsen_temperature_degC",
    "amundsen_salinity_psu",
    "amundsen_oxygen_uM",
    "amundsen_fluorescence_ug_l",
    "amundsen_nitrate_mmol_m3",
]


@dataclass(frozen=True)
class CtdContext:
    sample_id: int
    analysis_id: int
    deployment_id: int | None
    deployment_datetime: pd.Timestamp
    latitude: float
    longitude: float
    min_depth_m: float
    max_depth_m: float

    @property
    def mid_depth_m(self) -> float:
        return (self.min_depth_m + self.max_depth_m) / 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an agent-ready NeoLabs per-stage taxonomy table enriched with Amundsen CTD context."
    )
    parser.add_argument("--limit-contexts", type=int, default=None, help="Limit unique sample contexts for quick checks.")
    parser.add_argument("--output", type=Path, default=OUT, help="Output TSV path.")
    parser.add_argument("--refresh-cache", action="store_true", help="Ignore cached ERDDAP query files.")
    return parser.parse_args()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8", encoding_errors="replace")


def load_abundance_with_sample_metadata() -> pd.DataFrame:
    abundance = read_csv(ABUNDANCE_PATH)
    sample_metadata = read_csv(SAMPLE_METADATA_PATH)

    metadata_cols = [
        "sample_id",
        "analysis_id",
        "deployment_id",
        "sampling_platform",
        "deployment_datetime_start",
        "deployment_datetime_end",
        "latitude",
        "longitude",
        "bottom_depth",
        "deployment_comments",
        "NET_COMMENTS",
        "sample_comments",
    ]
    sample_metadata = sample_metadata[metadata_cols].drop_duplicates(["sample_id", "analysis_id"])

    merged = abundance.merge(
        sample_metadata,
        left_on=["SAMPLE_ID", "ANALYSIS_ID"],
        right_on=["sample_id", "analysis_id"],
        how="left",
    )
    merged["deployment_datetime_start"] = pd.to_datetime(
        merged["deployment_datetime_start"], errors="coerce", utc=True
    )
    for column in ["latitude", "longitude", "MIN_SAMPLE_DEPTH", "MAX_SAMPLE_DEPTH"]:
        merged[column] = pd.to_numeric(merged[column], errors="coerce")
    return merged


def iter_contexts(df: pd.DataFrame, limit: int | None = None) -> list[CtdContext]:
    cols = [
        "SAMPLE_ID",
        "ANALYSIS_ID",
        "deployment_id",
        "deployment_datetime_start",
        "latitude",
        "longitude",
        "MIN_SAMPLE_DEPTH",
        "MAX_SAMPLE_DEPTH",
    ]
    unique = df[cols].drop_duplicates(["SAMPLE_ID", "ANALYSIS_ID"])
    unique = unique.dropna(subset=["deployment_datetime_start", "latitude", "longitude", "MIN_SAMPLE_DEPTH", "MAX_SAMPLE_DEPTH"])
    if limit is not None:
        unique = unique.head(limit)

    contexts: list[CtdContext] = []
    for _, row in unique.iterrows():
        deployment_id = row.get("deployment_id")
        contexts.append(
            CtdContext(
                sample_id=int(row["SAMPLE_ID"]),
                analysis_id=int(row["ANALYSIS_ID"]),
                deployment_id=None if pd.isna(deployment_id) else int(deployment_id),
                deployment_datetime=row["deployment_datetime_start"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                min_depth_m=float(row["MIN_SAMPLE_DEPTH"]),
                max_depth_m=float(row["MAX_SAMPLE_DEPTH"]),
            )
        )
    return contexts


def cache_path(context: CtdContext, attempt: dict[str, Any]) -> Path:
    payload = {
        "sample_id": context.sample_id,
        "analysis_id": context.analysis_id,
        "deployment_datetime": context.deployment_datetime.isoformat(),
        "latitude": round(context.latitude, 5),
        "longitude": round(context.longitude, 5),
        "attempt": attempt,
    }
    digest = hashlib.sha1(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    return RAW / f"amundsen12713_{context.sample_id}_{context.analysis_id}_{attempt['label']}_{digest}.csv"


def erddap_query_url(context: CtdContext, attempt: dict[str, Any]) -> str:
    start = context.deployment_datetime - timedelta(hours=attempt["hours"])
    end = context.deployment_datetime + timedelta(hours=attempt["hours"])
    margin = attempt["margin_deg"]
    query = ",".join(ERDDAP_VARIABLES)
    query += f"&time>={start.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    query += f"&time<={end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    query += f"&latitude>={context.latitude - margin:.5f}&latitude<={context.latitude + margin:.5f}"
    query += f"&longitude>={context.longitude - margin:.5f}&longitude<={context.longitude + margin:.5f}"
    return f"{ERDDAP_URL}?{query}"


def query_ctd(context: CtdContext, refresh_cache: bool = False) -> tuple[pd.DataFrame, str | None]:
    if context.deployment_datetime < CTD_RANGE_START or context.deployment_datetime > CTD_RANGE_END:
        return pd.DataFrame(), "outside_amundsen_ctd_range"

    RAW.mkdir(parents=True, exist_ok=True)
    last_error: str | None = None
    for attempt in QUERY_ATTEMPTS:
        path = cache_path(context, attempt)
        if path.exists() and not refresh_cache:
            text = path.read_text(encoding="utf-8", errors="replace")
        else:
            response = requests.get(erddap_query_url(context, attempt), timeout=60)
            text = response.text
            if response.status_code == 404 and "query produced no matching results" in text:
                last_error = f"no_match_{attempt['label']}"
                continue
            response.raise_for_status()
            path.write_text(text, encoding="utf-8", errors="replace")

        ctd = pd.read_csv(StringIO(text)).rename(columns=CTD_RENAME)
        if not ctd.empty:
            ctd["ctd_query_attempt"] = attempt["label"]
            return normalize_ctd(ctd), None

    return pd.DataFrame(), last_error or "no_match"


def normalize_ctd(ctd: pd.DataFrame) -> pd.DataFrame:
    ctd["amundsen_time"] = pd.to_datetime(ctd["amundsen_time"], errors="coerce", utc=True)
    for column in ["amundsen_lat", "amundsen_lon", "amundsen_pres_db", "amundsen_depth_m", *CTD_VALUE_COLUMNS]:
        ctd[column] = pd.to_numeric(ctd[column], errors="coerce")
    return ctd.dropna(subset=["amundsen_time", "amundsen_lat", "amundsen_lon", "amundsen_depth_m"])


def haversine_km(lat1: float, lon1: float, lat2: pd.Series, lon2: pd.Series) -> pd.Series:
    radius_km = 6371.0
    lat1_rad = pd.Series(np.radians(lat1), index=lat2.index)
    lon1_rad = pd.Series(np.radians(lon1), index=lon2.index)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    return 2 * radius_km * np.arcsin(np.sqrt(a))


def select_cast(context: CtdContext, ctd: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["filename", "cast_number", "station"]
    casts = (
        ctd.groupby(group_cols, dropna=False)
        .agg(
            cast_time=("amundsen_time", "median"),
            cast_lat=("amundsen_lat", "median"),
            cast_lon=("amundsen_lon", "median"),
            cast_min_depth_m=("amundsen_depth_m", "min"),
            cast_max_depth_m=("amundsen_depth_m", "max"),
            cast_rows=("amundsen_depth_m", "size"),
        )
        .reset_index()
    )
    casts["ctd_time_delta_min"] = (
        casts["cast_time"] - context.deployment_datetime
    ).abs().dt.total_seconds() / 60
    casts["ctd_distance_km"] = haversine_km(context.latitude, context.longitude, casts["cast_lat"], casts["cast_lon"])
    casts["ctd_depth_coverage_m"] = (
        casts["cast_max_depth_m"].clip(upper=context.max_depth_m)
        - casts["cast_min_depth_m"].clip(lower=context.min_depth_m)
    ).clip(lower=0)
    casts["match_score"] = (
        casts["ctd_time_delta_min"] / 60
        + casts["ctd_distance_km"] / 10
        - casts["ctd_depth_coverage_m"] / 100
    )
    best = casts.sort_values(["match_score", "ctd_time_delta_min", "ctd_distance_km"]).iloc[0]
    mask = pd.Series(True, index=ctd.index)
    for column in group_cols:
        mask &= ctd[column].fillna("__NA__").eq(best[column] if pd.notna(best[column]) else "__NA__")
    selected = ctd[mask].copy()
    for column in ["ctd_time_delta_min", "ctd_distance_km", "ctd_depth_coverage_m"]:
        selected[column] = best[column]
    return selected


def summarize_context(context: CtdContext, ctd: pd.DataFrame, error: str | None) -> dict[str, Any]:
    base: dict[str, Any] = {
        "SAMPLE_ID": context.sample_id,
        "ANALYSIS_ID": context.analysis_id,
        "ctd_match_status": "matched" if error is None else error,
    }
    if error is not None or ctd.empty:
        return base

    selected = select_cast(context, ctd)
    interval = selected[
        (selected["amundsen_depth_m"] >= context.min_depth_m)
        & (selected["amundsen_depth_m"] <= context.max_depth_m)
    ].copy()
    if interval.empty:
        interval = selected.copy()
        base["ctd_match_status"] = "matched_cast_no_depth_interval_rows"

    nearest = selected.loc[(selected["amundsen_depth_m"] - context.mid_depth_m).abs().idxmin()]
    first = selected.iloc[0]
    base.update(
        {
            "amundsen_platform_name": first.get("platform_name"),
            "amundsen_filename": first.get("filename"),
            "amundsen_cruise_name": first.get("cruise_name"),
            "amundsen_cruise_number": first.get("cruise_number"),
            "amundsen_cast_number": first.get("cast_number"),
            "amundsen_station": first.get("station"),
            "ctd_query_attempt": first.get("ctd_query_attempt"),
            "ctd_time_delta_min": first.get("ctd_time_delta_min"),
            "ctd_distance_km": first.get("ctd_distance_km"),
            "ctd_depth_coverage_m": first.get("ctd_depth_coverage_m"),
            "ctd_rows_selected_cast": len(selected),
            "ctd_rows_in_sample_depth_interval": len(interval),
            "sample_mid_depth_m": context.mid_depth_m,
            "amundsen_nearest_depth_m": nearest.get("amundsen_depth_m"),
            "amundsen_nearest_depth_delta_m": abs(nearest.get("amundsen_depth_m") - context.mid_depth_m),
            "amundsen_nearest_time": nearest.get("amundsen_time"),
            "amundsen_nearest_lat": nearest.get("amundsen_lat"),
            "amundsen_nearest_lon": nearest.get("amundsen_lon"),
            "amundsen_nearest_pres_db": nearest.get("amundsen_pres_db"),
        }
    )
    for column in CTD_VALUE_COLUMNS:
        stem = column.removeprefix("amundsen_")
        base[f"{column}_nearest"] = nearest.get(column)
        base[f"amundsen_{stem}_mean_sample_interval"] = interval[column].mean()
        base[f"amundsen_{stem}_min_sample_interval"] = interval[column].min()
        base[f"amundsen_{stem}_max_sample_interval"] = interval[column].max()
    return base


def build_table(limit_contexts: int | None, refresh_cache: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    abundance = load_abundance_with_sample_metadata()
    contexts = iter_contexts(abundance, limit_contexts)

    summaries = []
    for index, context in enumerate(contexts, start=1):
        print(f"[{index}/{len(contexts)}] sample={context.sample_id} analysis={context.analysis_id}")
        ctd, error = query_ctd(context, refresh_cache=refresh_cache)
        summaries.append(summarize_context(context, ctd, error))

    ctd_summary = pd.DataFrame(summaries)
    enriched = abundance.merge(ctd_summary, on=["SAMPLE_ID", "ANALYSIS_ID"], how="left")
    enriched["ctd_match_status"] = enriched["ctd_match_status"].fillna("missing_sample_metadata")
    if limit_contexts is not None:
        keys = ctd_summary[["SAMPLE_ID", "ANALYSIS_ID"]].drop_duplicates()
        enriched = enriched.merge(keys, on=["SAMPLE_ID", "ANALYSIS_ID"], how="inner")
    return enriched, ctd_summary


def write_report(enriched: pd.DataFrame, ctd_summary: pd.DataFrame, output: Path) -> None:
    row_status_counts = enriched["ctd_match_status"].value_counts(dropna=False)
    context_status_counts = (
        enriched.drop_duplicates(["SAMPLE_ID", "ANALYSIS_ID"])["ctd_match_status"].value_counts(dropna=False)
    )
    output_label = str(output)
    try:
        output_label = str(output.relative_to(ROOT))
    except ValueError:
        pass
    lines = [
        "# NeoLabs per-stage taxonomy enriched with Amundsen CTD",
        "",
        f"- Output TSV: `{output_label}`",
        f"- Rows written: {len(enriched)}",
        f"- Unique sample/analysis contexts in output: {enriched.drop_duplicates(['SAMPLE_ID', 'ANALYSIS_ID']).shape[0]}",
        f"- Unique sample/analysis contexts checked against Amundsen: {len(ctd_summary)}",
        f"- Abundance source: `{ABUNDANCE_PATH.relative_to(ROOT)}`",
        f"- Sample metadata source: `{SAMPLE_METADATA_PATH.relative_to(ROOT)}`",
        f"- Amundsen CTD source: `{ERDDAP_URL}`",
        "",
        "CTD match statuses by context:",
        "",
    ]
    lines.extend(f"- `{status}`: {count}" for status, count in context_status_counts.items())
    lines.extend(["", "CTD match statuses by row:", ""])
    lines.extend(f"- `{status}`: {count}" for status, count in row_status_counts.items())
    lines.extend(
        [
            "",
            "Join logic:",
            "",
            "- NeoLabs per-stage abundances are joined to `donne_sample.csv` on `SAMPLE_ID` + `ANALYSIS_ID`.",
            "- ERDDAP CTD candidates are queried by deployment datetime and sample latitude/longitude.",
            "- The best CTD cast is selected by time delta, horizontal distance, and sampled-depth coverage.",
            "- CTD values are attached as nearest-mid-depth values plus mean/min/max over the sampled depth interval.",
            "- Samples outside the official Amundsen CTD time range are retained with `ctd_match_status=outside_amundsen_ctd_range`.",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    enriched, ctd_summary = build_table(args.limit_contexts, args.refresh_cache)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(args.output, sep="\t", index=False)
    write_report(enriched, ctd_summary, args.output)
    print(f"Wrote {args.output}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
