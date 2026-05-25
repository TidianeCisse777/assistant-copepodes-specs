from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
CLEAN = ROOT / "outputs" / "clean"
PROFILE_REPORT = ROOT / "outputs" / "column_null_profile.md"


def find_export_tsv() -> Path:
    tables = sorted((RAW / "export_unzipped").glob("*.tsv"))
    if not tables:
        raise FileNotFoundError(f"no TSV found under {RAW / 'export_unzipped'}")
    return tables[-1]


def profile_columns(df: pd.DataFrame) -> list[dict[str, object]]:
    rows = len(df)
    summary: list[dict[str, object]] = []
    for col in df.columns:
        series = df[col]
        nulls = int(series.isna().sum())
        non_null = rows - nulls
        sample = series.dropna().astype(str).drop_duplicates().head(3).tolist()
        summary.append(
            {
                "column": col,
                "nulls": nulls,
                "non_null": non_null,
                "null_pct": nulls / rows if rows else 0,
                "nunique": int(series.nunique(dropna=True)),
                "sample": sample,
            }
        )
    return summary


def write_profile_report(tsv_path: Path, rows: int, summary: list[dict[str, object]]) -> None:
    all_null = [item for item in summary if item["non_null"] == 0]
    constant = [item for item in summary if item["non_null"] > 0 and item["nunique"] <= 1]
    high_null = [item for item in summary if item["non_null"] > 0 and item["null_pct"] >= 0.90]
    variable = [item for item in summary if item["nunique"] > 1 and item["null_pct"] < 0.90]

    lines = [
        "# Profil null/constance des colonnes",
        "",
        f"TSV : `{tsv_path.name}`",
        f"Lignes : {rows}",
        f"Colonnes : {len(summary)}",
        "",
        "## Colonnes toujours nulles",
        "",
    ]
    lines.extend(f"- `{item['column']}`" for item in all_null)
    if not all_null:
        lines.append("- aucune")

    lines.extend(["", "## Colonnes constantes ou quasi non informatives", ""])
    for item in constant:
        lines.append(
            f"- `{item['column']}` : {item['non_null']} non null, {item['nulls']} null, "
            f"valeur unique = `{', '.join(item['sample'])}`"
        )
    if not constant:
        lines.append("- aucune")

    lines.extend(["", "## Colonnes avec au moins 90% de valeurs nulles", ""])
    for item in high_null:
        lines.append(
            f"- `{item['column']}` : {item['null_pct']:.1%} null, {item['non_null']} non null, "
            f"valeurs = `{', '.join(item['sample'])}`"
        )
    if not high_null:
        lines.append("- aucune")

    lines.extend(["", "## Colonnes variables avec moins de 90% de nulls", ""])
    for item in variable:
        lines.append(f"- `{item['column']}` : {item['null_pct']:.1%} null, {item['nunique']} valeurs distinctes")
    if not variable:
        lines.append("- aucune")

    PROFILE_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_clean_outputs(tsv_path: Path, df: pd.DataFrame, summary: list[dict[str, object]]) -> None:
    CLEAN.mkdir(parents=True, exist_ok=True)
    removed = [
        item["column"]
        for item in summary
        if item["non_null"] == 0 or item["nunique"] <= 1 or item["null_pct"] >= 0.90
    ]
    kept = [col for col in df.columns if col not in removed]
    clean_path = CLEAN / f"{tsv_path.stem}_clean.tsv"
    df[kept].to_csv(clean_path, sep="\t", index=False)
    payload = {
        "source_tsv": str(tsv_path),
        "rows": int(len(df)),
        "original_column_count": int(len(df.columns)),
        "removed_column_count": len(removed),
        "remaining_column_count": len(kept),
        "removed_columns": removed,
        "clean_tsv": str(clean_path),
    }
    (CLEAN / "removed_columns.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    tsv_path = find_export_tsv()
    df = pd.read_csv(tsv_path, sep="\t", low_memory=False, na_values=["", "NA", "NaN", "nan", "None", "null"])
    summary = profile_columns(df)
    write_profile_report(tsv_path, len(df), summary)
    write_clean_outputs(tsv_path, df, summary)
    print(f"Profiled {len(df)} rows, wrote {PROFILE_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
