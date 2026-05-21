from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples_tsv"
OUT = EXAMPLES / "uvp_amundsen_1165_105_enriched_nearest_depth.tsv"
REPORT = ROOT / "ecopart_1165_link_probe" / "outputs" / "report_depth_enriched_table.md"

ECOTAXA_PATH = EXAMPLES / "uvp_amundsen_1165_ecotaxa_object_sample.tsv"
ECOPART_PATH = EXAMPLES / "uvp_amundsen_105_ecopart_particles_reduced.tsv"


def extract_profile_id(obj_orig_id: object) -> str | None:
    parts = str(obj_orig_id).split("_")
    if len(parts) >= 2:
        return "_".join(parts[:2])
    return None


def midpoint_depth(row: pd.Series) -> float:
    depth_min = pd.to_numeric(row.get("obj_depth_min"), errors="coerce")
    depth_max = pd.to_numeric(row.get("obj_depth_max"), errors="coerce")
    if pd.notna(depth_min) and pd.notna(depth_max):
        return float((depth_min + depth_max) / 2)
    if pd.notna(depth_min):
        return float(depth_min)
    return float(depth_max)


def nearest_ecopart_row(object_row: pd.Series, ecopart_group: pd.DataFrame) -> pd.Series | None:
    if ecopart_group.empty or pd.isna(object_row["object_depth"]):
        return None
    deltas = (ecopart_group["ecopart_depth"] - object_row["object_depth"]).abs()
    return ecopart_group.loc[deltas.idxmin()]


def depth_match_quality(object_depth: float, ecopart_depth: float, profile_depth_min: float, profile_depth_max: float) -> str:
    delta = abs(object_depth - ecopart_depth)
    if object_depth < profile_depth_min or object_depth > profile_depth_max:
        return "outside_ecopart_sample_range"
    if delta <= 2.5:
        return "within_5m_bin"
    if delta <= 10:
        return "near"
    return "coarse"


def main() -> int:
    ecotaxa = pd.read_csv(ECOTAXA_PATH, sep="\t")
    ecopart = pd.read_csv(ECOPART_PATH, sep="\t")

    ecotaxa["profile_id"] = ecotaxa["obj_orig_id"].map(extract_profile_id)
    ecotaxa["object_depth"] = ecotaxa.apply(midpoint_depth, axis=1)

    ecopart = ecopart.rename(
        columns={
            "Profile": "profile_id",
            "Depth [m]": "ecopart_depth",
            "yyyy-mm-dd hh:mm": "ecopart_datetime",
            "temperature [degc]": "ecopart_temperature_degC",
            "practical salinity [psu]": "ecopart_salinity_psu",
            "oxygen [umol kg-1]": "ecopart_oxygen_umol_kg",
            "oxygen [ml l-1]": "ecopart_oxygen_ml_l",
            "chloro fluo [mg chl m-3]": "ecopart_fluorescence_mg_chl_m3",
            "nitrate [umol l-1]": "ecopart_nitrate_umol_l",
            "pressure [db]": "ecopart_pressure_db",
            "Sampled volume [L]": "ecopart_sampled_volume_l",
            "Project": "ecopart_project",
            "Rawfilename": "ecopart_rawfilename",
        }
    )
    ecopart["ecopart_depth"] = pd.to_numeric(ecopart["ecopart_depth"], errors="coerce")

    particle_cols = [
        "LPM (64-128 µm) [# l-1]",
        "LPM (128-256 µm) [# l-1]",
        "LPM (256-512 µm) [# l-1]",
        "LPM (0.512-1.02 mm) [# l-1]",
        "LPM (1.02-2.05 mm) [# l-1]",
        "LPM biovolume (64-128 µm) [mm3 l-1]",
        "LPM biovolume (128-256 µm) [mm3 l-1]",
        "LPM biovolume (256-512 µm) [mm3 l-1]",
        "LPM biovolume (0.512-1.02 mm) [mm3 l-1]",
        "LPM biovolume (1.02-2.05 mm) [mm3 l-1]",
    ]
    for col in particle_cols:
        if col in ecopart.columns:
            ecopart[col] = pd.to_numeric(ecopart[col], errors="coerce")
    count_cols = [col for col in particle_cols if "[# l-1]" in col and col in ecopart.columns]
    biovol_cols = [col for col in particle_cols if "[mm3 l-1]" in col and col in ecopart.columns]
    ecopart["ecopart_particle_count_l_selected_sum"] = ecopart[count_cols].sum(axis=1, min_count=1)
    ecopart["ecopart_particle_biovolume_selected_sum"] = ecopart[biovol_cols].sum(axis=1, min_count=1)

    ecopart_by_profile = {
        profile_id: group.copy()
        for profile_id, group in ecopart.groupby("profile_id", dropna=True)
    }

    rows = []
    for _, object_row in ecotaxa.iterrows():
        profile_id = object_row["profile_id"]
        ecopart_group = ecopart_by_profile.get(profile_id, pd.DataFrame())
        nearest = nearest_ecopart_row(object_row, ecopart_group)
        row = {
            "object_id": object_row.get("object_id"),
            "obj_orig_id": object_row.get("obj_orig_id"),
            "profile_id": profile_id,
            "sample_id": object_row.get("sample_id"),
            "taxon": object_row.get("txo_display_name"),
            "object_depth": object_row.get("object_depth"),
            "obj_objdate": object_row.get("obj_objdate"),
            "obj_objtime": object_row.get("obj_objtime"),
            "obj_latitude": object_row.get("obj_latitude"),
            "obj_longitude": object_row.get("obj_longitude"),
            "fre_area": object_row.get("fre_area"),
            "fre_esd": object_row.get("fre_esd"),
            "fre_feret": object_row.get("fre_feret"),
            "fre_major": object_row.get("fre_major"),
            "fre_minor": object_row.get("fre_minor"),
            "match_method": "profile_id+nearest_depth" if nearest is not None else "unmatched",
        }
        if nearest is not None:
            profile_depth_min = float(ecopart_group["ecopart_depth"].min())
            profile_depth_max = float(ecopart_group["ecopart_depth"].max())
            depth_delta = abs(float(object_row["object_depth"]) - float(nearest["ecopart_depth"]))
            row.update(
                {
                    "ecopart_depth": nearest.get("ecopart_depth"),
                    "depth_delta_m": depth_delta,
                    "ecopart_profile_depth_min": profile_depth_min,
                    "ecopart_profile_depth_max": profile_depth_max,
                    "depth_match_quality": depth_match_quality(
                        float(object_row["object_depth"]),
                        float(nearest["ecopart_depth"]),
                        profile_depth_min,
                        profile_depth_max,
                    ),
                    "ecopart_datetime": nearest.get("ecopart_datetime"),
                    "ecopart_temperature_degC": nearest.get("ecopart_temperature_degC"),
                    "ecopart_salinity_psu": nearest.get("ecopart_salinity_psu"),
                    "ecopart_oxygen_umol_kg": nearest.get("ecopart_oxygen_umol_kg"),
                    "ecopart_oxygen_ml_l": nearest.get("ecopart_oxygen_ml_l"),
                    "ecopart_fluorescence_mg_chl_m3": nearest.get("ecopart_fluorescence_mg_chl_m3"),
                    "ecopart_nitrate_umol_l": nearest.get("ecopart_nitrate_umol_l"),
                    "ecopart_pressure_db": nearest.get("ecopart_pressure_db"),
                    "ecopart_sampled_volume_l": nearest.get("ecopart_sampled_volume_l"),
                    "ecopart_particle_count_l_selected_sum": nearest.get("ecopart_particle_count_l_selected_sum"),
                    "ecopart_particle_biovolume_selected_sum": nearest.get("ecopart_particle_biovolume_selected_sum"),
                }
            )
        rows.append(row)

    enriched = pd.DataFrame(rows)
    enriched.to_csv(OUT, sep="\t", index=False)

    matched = int((enriched["match_method"] != "unmatched").sum())
    total = len(enriched)
    max_delta = enriched["depth_delta_m"].max()
    median_delta = enriched["depth_delta_m"].median()
    quality_counts = enriched["depth_match_quality"].value_counts(dropna=False).to_dict()

    lines = [
        "# EcoTaxa 1165 + EcoPart 105 depth-enriched table",
        "",
        f"- Objets EcoTaxa: {total}",
        f"- Objets enrichis avec EcoPart: {matched}/{total}",
        f"- Methode: `profile_id + profondeur EcoPart la plus proche`",
        f"- Delta profondeur median: {median_delta:.3f} m",
        f"- Delta profondeur max: {max_delta:.3f} m",
        f"- Qualite des matchs profondeur: {quality_counts}",
        f"- Sortie TSV: `{OUT.relative_to(ROOT)}`",
        "",
        "Colonnes ajoutees depuis EcoPart:",
        "",
        "- `ecopart_depth`",
        "- `depth_delta_m`",
        "- `depth_match_quality`",
        "- `ecopart_temperature_degC`",
        "- `ecopart_salinity_psu`",
        "- `ecopart_oxygen_umol_kg` / `ecopart_oxygen_ml_l`",
        "- `ecopart_fluorescence_mg_chl_m3`",
        "- `ecopart_nitrate_umol_l`",
        "- `ecopart_particle_count_l_selected_sum`",
        "- `ecopart_particle_biovolume_selected_sum`",
        "",
        "Limite: ce test utilise les extraits TSV conserves, pas les exports complets. Les lignes `outside_ecopart_sample_range` indiquent que l'objet est plus profond que l'extrait EcoPart disponible.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
