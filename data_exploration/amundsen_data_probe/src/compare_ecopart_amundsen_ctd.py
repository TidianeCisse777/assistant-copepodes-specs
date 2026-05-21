from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples_tsv"
RAW = ROOT / "amundsen_data_probe" / "outputs" / "raw"
REPORT = ROOT / "amundsen_data_probe" / "outputs" / "report_ecopart_amundsen_compare.md"

JOIN_PREVIEW = EXAMPLES / "uvp_amundsen_1165_105_join_preview.tsv"
ECOPART_PARTICLES = EXAMPLES / "uvp_amundsen_105_ecopart_particles_reduced.tsv"
AMUNDSEN_MATCH_SAMPLE = EXAMPLES / "amundsen_12713_ctd_ips007_match_sample.tsv"
COMPARE_OUT = EXAMPLES / "uvp_amundsen_105_ecopart_vs_amundsen_ctd_compare.tsv"

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


def query_amundsen_ctd(profile_metadata: pd.Series) -> pd.DataFrame:
    date = str(profile_metadata["ecopart_date"])
    lat = float(profile_metadata["ecopart_lat"])
    lon = float(profile_metadata["ecopart_lon"])
    margin = 0.3
    query = ",".join(ERDDAP_VARIABLES)
    query += f"&time>={date}T00:00:00Z&time<={date}T23:59:59Z"
    query += f"&latitude>={lat - margin}&latitude<={lat + margin}"
    query += f"&longitude>={lon - margin}&longitude<={lon + margin}"
    url = f"{ERDDAP_URL}?{query}"

    response = requests.get(url, timeout=60)
    response.raise_for_status()
    raw_path = RAW / "amundsen12713_ips007_match_query.csv"
    raw_path.write_text(response.text, encoding="utf-8", errors="replace")

    return pd.read_csv(raw_path)


def normalize_amundsen_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(
        columns={
            "time (UTC)": "amundsen_time",
            "latitude (degrees_north)": "amundsen_lat",
            "longitude (degrees_east)": "amundsen_lon",
            "PRES (decibars)": "amundsen_pres_db",
            "depth (m)": "amundsen_depth",
            "TE90 (degC)": "amundsen_temperature_degC",
            "PSAL (PSU)": "amundsen_salinity_psu",
            "OXYM (uM)": "amundsen_oxygen_uM",
            "FLOR (ug/L)": "amundsen_fluorescence_ug_l",
            "NTRA (mmol/m^3)": "amundsen_nitrate_mmol_m3",
        }
    )


def normalize_ecopart_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(
        columns={
            "Profile": "profile_id",
            "yyyy-mm-dd hh:mm": "ecopart_datetime",
            "Depth [m]": "ecopart_depth",
            "temperature [degc]": "ecopart_temperature_degC",
            "practical salinity [psu]": "ecopart_salinity_psu",
            "oxygen [umol kg-1]": "ecopart_oxygen_umol_kg",
            "chloro fluo [mg chl m-3]": "ecopart_fluorescence_mg_chl_m3",
            "nitrate [umol l-1]": "ecopart_nitrate_umol_l",
            "pressure [db]": "ecopart_pressure_db",
        }
    )


def nearest_amundsen_row(ecopart_row: pd.Series, amundsen: pd.DataFrame) -> pd.Series:
    deltas = (amundsen["amundsen_depth"] - ecopart_row["ecopart_depth"]).abs()
    return amundsen.loc[deltas.idxmin()]


def main() -> int:
    join_preview = pd.read_csv(JOIN_PREVIEW, sep="\t")
    profile_metadata = join_preview.drop_duplicates("profile_id").iloc[0]
    profile_id = profile_metadata["profile_id"]

    amundsen = normalize_amundsen_columns(query_amundsen_ctd(profile_metadata))
    amundsen["amundsen_depth"] = pd.to_numeric(amundsen["amundsen_depth"], errors="coerce")
    amundsen.to_csv(AMUNDSEN_MATCH_SAMPLE, sep="\t", index=False)

    ecopart = normalize_ecopart_columns(pd.read_csv(ECOPART_PARTICLES, sep="\t"))
    ecopart = ecopart[ecopart["profile_id"] == profile_id].copy()
    ecopart["ecopart_depth"] = pd.to_numeric(ecopart["ecopart_depth"], errors="coerce")

    rows = []
    for _, ecopart_row in ecopart.iterrows():
        nearest = nearest_amundsen_row(ecopart_row, amundsen)
        rows.append(
            {
                "profile_id": profile_id,
                "ecopart_datetime": ecopart_row.get("ecopart_datetime"),
                "ecopart_depth": ecopart_row.get("ecopart_depth"),
                "amundsen_cast_number": nearest.get("cast_number"),
                "amundsen_station": nearest.get("station"),
                "amundsen_time": nearest.get("amundsen_time"),
                "amundsen_depth": nearest.get("amundsen_depth"),
                "depth_delta_m": abs(ecopart_row.get("ecopart_depth") - nearest.get("amundsen_depth")),
                "ecopart_temperature_degC": ecopart_row.get("ecopart_temperature_degC"),
                "amundsen_temperature_degC": nearest.get("amundsen_temperature_degC"),
                "temperature_delta_degC": ecopart_row.get("ecopart_temperature_degC") - nearest.get("amundsen_temperature_degC"),
                "ecopart_salinity_psu": ecopart_row.get("ecopart_salinity_psu"),
                "amundsen_salinity_psu": nearest.get("amundsen_salinity_psu"),
                "ecopart_fluorescence_mg_chl_m3": ecopart_row.get("ecopart_fluorescence_mg_chl_m3"),
                "amundsen_fluorescence_ug_l": nearest.get("amundsen_fluorescence_ug_l"),
                "ecopart_pressure_db": ecopart_row.get("ecopart_pressure_db"),
                "amundsen_pres_db": nearest.get("amundsen_pres_db"),
                "amundsen_lat": nearest.get("amundsen_lat"),
                "amundsen_lon": nearest.get("amundsen_lon"),
                "ecopart_lat": profile_metadata.get("ecopart_lat"),
                "ecopart_lon": profile_metadata.get("ecopart_lon"),
            }
        )

    compare = pd.DataFrame(rows)
    compare.to_csv(COMPARE_OUT, sep="\t", index=False)

    amundsen_time = pd.to_datetime(amundsen["amundsen_time"].iloc[0], utc=True)
    ecopart_time = pd.to_datetime(
        str(profile_metadata["ecopart_date"]) + " " + str(profile_metadata["ecopart_time"]),
        utc=True,
    )
    time_delta_min = abs((amundsen_time - ecopart_time).total_seconds()) / 60
    lat_delta = abs(float(profile_metadata["ecopart_lat"]) - float(amundsen["amundsen_lat"].iloc[0]))
    lon_delta = abs(float(profile_metadata["ecopart_lon"]) - float(amundsen["amundsen_lon"].iloc[0]))

    lines = [
        "# EcoPart 105 vs Amundsen official CTD",
        "",
        f"- Profile EcoPart teste: `{profile_id}`",
        f"- Temps EcoPart: {profile_metadata['ecopart_date']} {profile_metadata['ecopart_time']}",
        f"- Cast Amundsen trouve: `{amundsen['cast_number'].iloc[0]}` station `{amundsen['station'].iloc[0]}`",
        f"- Temps Amundsen: {amundsen['amundsen_time'].iloc[0]}",
        f"- Delta temps: {time_delta_min:.2f} minutes",
        f"- Delta latitude: {lat_delta:.6f}",
        f"- Delta longitude: {lon_delta:.6f}",
        f"- Lignes CTD Amundsen recuperees: {len(amundsen)}",
        f"- Lignes EcoPart comparees: {len(compare)}",
        f"- Delta profondeur median: {compare['depth_delta_m'].median():.3f} m",
        f"- Delta profondeur max: {compare['depth_delta_m'].max():.3f} m",
        "",
        "Fichiers generes:",
        "",
        f"- `{AMUNDSEN_MATCH_SAMPLE.relative_to(ROOT)}`",
        f"- `{COMPARE_OUT.relative_to(ROOT)}`",
        "",
        "Conclusion:",
        "",
        "- Le cast CTD officiel Amundsen correspondant au profil EcoPart existe dans ERDDAP.",
        "- La comparaison directe est possible via date/time + lat/lon + profondeur proche.",
        "- Ce test reste leger : il compare seulement le profil `ips_007` conserve dans les extraits.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {AMUNDSEN_MATCH_SAMPLE}")
    print(f"Wrote {COMPARE_OUT}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
