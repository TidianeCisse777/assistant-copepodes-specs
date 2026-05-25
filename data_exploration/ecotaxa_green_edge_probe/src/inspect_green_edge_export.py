from __future__ import annotations

import csv
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd


PROJECT_ID = 42
PROJECT_LABEL = "UVP5 GREEN EDGE Ice Camp 2015"
ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
RAW = OUTPUTS / "raw"
REPORT = OUTPUTS / "report.md"
DEFAULT_EXPORT = RAW / "ecotaxa_green_edge_42_export.zip"


def normalize_field(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def useful_field_presence(columns: list[str]) -> dict[str, bool]:
    normalized = {normalize_field(col) for col in columns}
    date_time_fields = {
        "date_time",
        "datetime",
        "date",
        "acq_date",
        "acquisition_date",
        "sample_date",
        "sampling_date",
        "object_date",
    }
    return {
        "object_id": any("object_id" in col or col == "object" for col in normalized),
        "object_orig_id": any("obj_orig_id" in col or "object_orig_id" in col for col in normalized),
        "sample_id": any("sample_id" in col or col == "sample" for col in normalized),
        "taxon": any("taxon" in col or "classif" in col or "txo" in col for col in normalized),
        "station/location": any("station" in col or "location" in col for col in normalized),
        "date_time/date": any(col in date_time_fields for col in normalized),
        "depth": any("depth" in col for col in normalized),
        "lat/lon": any("lat" in col or "latitude" in col for col in normalized)
        and any("lon" in col or "longitude" in col for col in normalized),
        "validation status": any("status" in col or "valid" in col for col in normalized),
        "uvp_morphometry": any(col.startswith("object_") or col.startswith("fre_") for col in normalized),
    }


def sniff_separator(path: Path) -> str:
    sample = path.read_text(encoding="utf-8", errors="replace")[:4096]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        return "\t" if path.suffix.lower() == ".tsv" else ","


def find_tables(extract_dir: Path) -> list[Path]:
    suffixes = {".csv", ".tsv", ".txt"}
    return sorted(path for path in extract_dir.rglob("*") if path.is_file() and path.suffix.lower() in suffixes)


def read_preview(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=sniff_separator(path), nrows=100, low_memory=False)


def write_report(columns: list[str], tables: list[Path]) -> None:
    useful = useful_field_presence(columns)
    lines = [
        f"EcoTaxa authenticated export inspection - project {PROJECT_ID}",
        "",
        f"Projet confirme : {PROJECT_LABEL}",
        "",
        "Colonnes detectees :",
    ]
    lines.extend(f"- {column}" for column in columns) if columns else lines.append("- aucune colonne detectee")
    lines.extend(["", "Champs utiles detectes :"])
    for field, present in useful.items():
        lines.append(f"- {field} : {'oui' if present else 'non'}")
    lines.extend(["", "Tables inspectees :"])
    lines.extend(f"- {table.relative_to(ROOT)}" for table in tables) if tables else lines.append("- aucune")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    export_path = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_EXPORT
    if not export_path.exists():
        print(f"No export ZIP found at {export_path}")
        return 1

    extract_dir = RAW / "export_unzipped"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(export_path) as zf:
        zf.extractall(extract_dir)

    tables = find_tables(extract_dir)
    all_columns: list[str] = []
    previews: dict[str, list[dict[str, object]]] = {}

    for table in tables:
        try:
            df = read_preview(table)
        except Exception as exc:
            previews[str(table.relative_to(ROOT))] = [{"error": str(exc)}]
            continue
        for column in df.columns:
            if column not in all_columns:
                all_columns.append(str(column))
        preview_path = RAW / f"preview_{table.stem}.csv"
        df.head(100).to_csv(preview_path, index=False)
        previews[str(table.relative_to(ROOT))] = df.head(5).where(pd.notna(df.head(5)), None).to_dict(orient="records")

    (RAW / "export_columns.json").write_text(json.dumps(all_columns, indent=2, ensure_ascii=False), encoding="utf-8")
    (RAW / "export_previews.json").write_text(
        json.dumps(previews, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    write_report(all_columns, tables)
    print(f"Inspected {len(tables)} table(s), wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
