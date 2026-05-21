from __future__ import annotations

import csv
import json
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
JOIN_CSV = ROOT / "outputs" / "join_preview_ecotaxa1165_ecopart105.csv"
REPORT = ROOT / "outputs" / "report_join_test.md"
ECOPART_BASE = "https://ecopart.obs-vlfr.fr"


def strip_html(html: str) -> str:
    return re.sub(r"\s+", " ", BeautifulSoup(html, "html.parser").get_text(" ", strip=True)).strip()


def parse_popover(text: str) -> dict[str, Any]:
    patterns = {
        "ecopart_sample_id": r"ID\s*:\s*(\d+)",
        "profile_id": r"Profile ID\s*:\s*([^ ]+)",
        "ecopart_project": r"Project\s*:\s*(.+?)\s+Ship\s*:",
        "ship": r"Ship\s*:\s*(.+?)\s+Cruise\s*:",
        "cruise": r"Cruise\s*:\s*(.+?)\s+Ecotaxa Project\s*:",
        "ecotaxa_project": r"Ecotaxa Project\s*:\s*(.+?)\s+Lat/Lon\s*:",
        "lat_lon": r"Lat/Lon\s*:\s*([-\d.]+)/([-\d.]+)",
        "date_time": r"Date/Time\s*:\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})",
    }
    out: dict[str, Any] = {"raw": text}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if not match:
            continue
        if key == "lat_lon":
            out["ecopart_lat"] = float(match.group(1))
            out["ecopart_lon"] = float(match.group(2))
        elif key == "date_time":
            out["ecopart_date"] = match.group(1)
            out["ecopart_time"] = match.group(2)
        elif key == "ecopart_sample_id":
            out[key] = int(match.group(1))
        else:
            out[key] = match.group(1).strip()
    return out


def fetch_popover(sample_id: int, session: requests.Session) -> dict[str, Any]:
    path = RAW / f"ecopart_sample_{sample_id}_popover.html"
    if path.exists():
        html = path.read_text(encoding="utf-8", errors="replace")
    else:
        response = session.get(f"{ECOPART_BASE}/getsamplepopover/{sample_id}", timeout=60)
        response.raise_for_status()
        html = response.text
        path.write_text(html, encoding="utf-8")
        time.sleep(1)
    return parse_popover(strip_html(html))


def extract_profile_id(obj_orig_id: str) -> str | None:
    parts = str(obj_orig_id).split("_")
    if len(parts) >= 2:
        return "_".join(parts[:2])
    return None


def load_or_fetch_ecopart_profiles() -> pd.DataFrame:
    samples_path = RAW / "ecopart_105_samples.csv"
    samples = pd.read_csv(samples_path)
    session = requests.Session()
    session.headers.update({"User-Agent": "ecopart-1165-join-test/0.1"})
    rows = []
    for sample_id in samples["id"].tolist():
        row = fetch_popover(int(sample_id), session)
        row["visibility"] = samples.loc[samples["id"] == sample_id, "visibility"].iloc[0]
        rows.append(row)
    profile_df = pd.DataFrame(rows)
    profile_df.to_csv(RAW / "ecopart_105_profiles_from_popovers.csv", index=False)
    return profile_df


def main() -> int:
    ecotaxa = pd.read_csv(RAW / "ecotaxa_1165_query_sample.csv")
    ecotaxa["profile_id"] = ecotaxa["obj_orig_id"].map(extract_profile_id)

    profiles = load_or_fetch_ecopart_profiles()
    joined = ecotaxa.merge(profiles, on="profile_id", how="left", suffixes=("_ecotaxa", "_ecopart"))
    joined["lat_delta"] = (joined["obj_latitude"] - joined["ecopart_lat"]).abs()
    joined["lon_delta"] = (joined["obj_longitude"] - joined["ecopart_lon"]).abs()
    joined["date_match"] = joined["obj_objdate"] == joined["ecopart_date"]

    keep_cols = [
        "object_id",
        "obj_orig_id",
        "profile_id",
        "ecopart_sample_id",
        "sample_id",
        "project_id",
        "obj_depth_min",
        "obj_depth_max",
        "obj_objdate",
        "obj_objtime",
        "ecopart_date",
        "ecopart_time",
        "obj_latitude",
        "obj_longitude",
        "ecopart_lat",
        "ecopart_lon",
        "lat_delta",
        "lon_delta",
        "date_match",
        "fre_area",
        "fre_major",
        "fre_minor",
        "fre_feret",
        "fre_esd",
        "fre_width",
        "fre_height",
        "txo_display_name",
    ]
    joined[keep_cols].to_csv(JOIN_CSV, index=False)

    matched = int(joined["ecopart_sample_id"].notna().sum())
    total = len(joined)
    max_lat_delta = joined["lat_delta"].max()
    max_lon_delta = joined["lon_delta"].max()
    date_matches = int(joined["date_match"].sum())

    lines = [
        "Minimal join test — EcoTaxa 1165 + EcoPart 105",
        "",
        f"1. Objets EcoTaxa testes : {total}",
        f"2. Objets relies a un profile_id EcoPart : {matched}/{total}",
        f"3. Profils EcoPart disponibles : {profiles['profile_id'].nunique()}",
        f"4. Dates concordantes : {date_matches}/{total}",
        f"5. Delta lat max : {max_lat_delta}",
        f"6. Delta lon max : {max_lon_delta}",
        "7. Cle utilisee :",
        "   - extraire profile_id depuis EcoTaxa obj_orig_id, ex. ips_007_899 -> ips_007",
        "   - joindre avec EcoPart profile_id issu de getsamplepopover",
        "8. Colonnes ajoutees cote EcoPart :",
        "   - ecopart_sample_id",
        "   - ecopart_lat / ecopart_lon",
        "   - ecopart_date / ecopart_time",
        "   - ship / cruise / ecopart_project / ecotaxa_project",
        "9. Conclusion :",
        f"   - jointure structurelle valide ? {'oui' if matched == total and date_matches == total else 'partielle'}",
        "   - prochaine etape : obtenir/exporter les tables EcoPart CTD/particules pour joindre par profile_id + profondeur",
        "",
        f"Fichier jointure : {JOIN_CSV.relative_to(ROOT)}",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {JOIN_CSV}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
