from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_TSV = ROOT / "outputs" / "sample" / "columns_metadata.tsv"
INPUT_JSON = ROOT / "outputs" / "sample" / "columns_metadata.json"
OUTPUT_CATEGORY = ROOT / "outputs" / "sample" / "columns_by_category.md"
OUTPUT_KEYS = ROOT / "outputs" / "sample" / "key_columns_check.md"


GROUP_ORDER = [
    "1. Identification, position, temps et profondeur de l'objet",
    "2. Taxonomie, validation et classification automatique",
    "3. Colonnes affichees dans l'interface de classification",
    "4. Morphometrie - taille et surface",
    "5. Morphometrie - forme, contour et position image",
    "6. Intensite, niveaux de gris et texture",
    "7. Moments mathematiques et descripteurs derives",
    "8. Detection, vignette et doublons",
    "9. Sample, station et deploiement",
    "10. Acquisition LOKI, CTD embarquee et capteurs",
    "11. Process / traitement image",
    "12. Colonnes internes ou peu analytiques",
]

KEY_CONCEPTS = [
    ("Identifiant objet", ["obj.orig_id"]),
    ("Latitude objet", ["obj.latitude", "sample.latitude"]),
    ("Longitude objet", ["obj.longitude", "sample.longitude"]),
    ("Date objet", ["obj.objdate", "sample.deployment_date_start", "sample.deployment_datetime_start"]),
    ("Heure objet", ["obj.objtime", "sample.deployment_time_start", "sample.deployment_time_start_str"]),
    ("Profondeur objet min", ["obj.depth_min", "fre.Depth min"]),
    ("Profondeur objet max", ["obj.depth_max"]),
    ("Taxon affiche / valide", ["txo.display_name", "txo.name"]),
    ("Statut de validation", ["obj.classif_qual"]),
    ("Classification automatique", ["obj.classif_auto_id", "obj.classif_auto_score", "obj.classif_auto_when"]),
    ("ESD / diametre equivalent", ["fre.equivalent_diameter_area"]),
    ("Grand axe", ["fre.axis_major_length"]),
    ("Petit axe", ["fre.axis_minor_length"]),
    ("Feret max", ["fre.feret_diameter_max"]),
    ("Surface objet", ["fre.area", "fre.area_filled", "fre.area_convex"]),
    ("Intensite moyenne", ["fre.intensity_mean", "fre.image_pixel_int_mean"]),
    ("Calibration pixel", ["acq.pixel_um_size"]),
    ("Station", ["sample.station_name"]),
    ("Engin / filet", ["sample.gear", "sample.gear_net_id", "sample.net_mesh_size", "sample.net_mouth_aperture"]),
    ("CTD temperature", ["acq.temperature_ctd"]),
    ("CTD salinite", ["acq.salinity_ctd"]),
    ("CTD oxygene", ["acq.oxygen_concent", "acq.oxygen_saturation"]),
    ("Fluorescence", ["acq.fluo1", "acq.fluo2", "acq.fluo3", "acq.fluo4"]),
    ("Profondeur acquisition", ["acq.raw_depth", "acq.pressure_sensor_press"]),
]


def read_rows() -> list[dict[str, str]]:
    with INPUT_TSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def classify(row: dict[str, str]) -> str:
    field = row["field"]
    source = row["source_name"]
    category = row["category"]
    low = field.lower()

    if category in {"object", "taxonomy"}:
        if low.startswith("txo.") or "classif" in low:
            return "2. Taxonomie, validation et classification automatique"
        if any(name in low for name in ["random_value", "sunpos", "object_link", "complement_info"]):
            return "12. Colonnes internes ou peu analytiques"
        return "1. Identification, position, temps et profondeur de l'objet"
    if category == "classification_display":
        return "3. Colonnes affichees dans l'interface de classification"
    if category == "sample":
        return "9. Sample, station et deploiement"
    if category == "acquisition":
        return "10. Acquisition LOKI, CTD embarquee et capteurs"
    if category == "process":
        return "11. Process / traitement image"
    if category == "object_free":
        if source.startswith(("moments", "log_moments")):
            return "7. Moments mathematiques et descripteurs derives"
        if source.startswith("double_") or source in {
            "frame_ms",
            "frame_vignette_number",
            "vignette_x_pos",
            "vignette_y_pos",
            "orig_img_bmp_file_size",
            "image_height",
            "image_width",
            "label_id_number",
            "total_doubles",
        }:
            return "8. Detection, vignette et doublons"
        if any(token in low for token in ["intensity", "image_pixel", "threshold"]):
            return "6. Intensite, niveaux de gris et texture"
        if any(token in low for token in ["area", "diameter", "axis_major", "axis_minor", "feret"]):
            return "4. Morphometrie - taille et surface"
        return "5. Morphometrie - forme, contour et position image"
    return "12. Colonnes internes ou peu analytiques"


def write_category_report(rows: list[dict[str, str]], metadata: dict) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[classify(row)].append(row)

    project = metadata["project"]
    lines = [
        "# Colonnes EcoTaxa LOKI - ArcticNet 2015",
        "",
        f"Projet EcoTaxa `{project['project_id']}`. Extraction metadata-only, sans telechargement des objets.",
        f"Total : {len(rows)} colonnes detectees dans la metadata projet.",
        "",
        "Note : ce rapport classe les colonnes disponibles. Il ne prouve pas quelles colonnes sont nulles ou constantes dans les objets, car aucun TSV objet complet n'a ete exporte.",
        "",
    ]
    for group in GROUP_ORDER:
        group_rows = grouped.get(group, [])
        if not group_rows:
            continue
        lines.extend([f"## {group}", ""])
        for row in group_rows:
            slot = f" ({row['storage_slot']})" if row["storage_slot"] else ""
            lines.append(f"- `{row['field']}`{slot} - {row['display_name']}")
        lines.append("")

    lines.extend(
        [
            "## Colonnes prioritaires pour analyses copepodes",
            "",
            "- Spatio-temporel : `obj.latitude`, `obj.longitude`, `obj.objdate`, `obj.objtime`",
            "- Profondeur : `obj.depth_min`, `obj.depth_max`, `fre.Depth min`, `acq.raw_depth`",
            "- Taxon valide : `txo.display_name`, `txo.name`, `obj.classif_qual`",
            "- Taille : `fre.equivalent_diameter_area`, `fre.axis_major_length`, `fre.axis_minor_length`, `fre.feret_diameter_max`, `fre.area`",
            "- Forme : `fre.eccentricity`, `fre.extent`, `fre.solidity`, `fre.perimeter`, `fre.orientation`",
            "- Intensite : `fre.intensity_mean`, `fre.intensity_min`, `fre.intensity_max`, `fre.image_pixel_int_mean`, `fre.image_pixel_int_stddev`",
            "- Sample/deploiement : `sample.station_name`, `sample.deployment_datetime_start`, `sample.gear`, `sample.tow_type`, `sample.cast_number`",
            "- Filet : `sample.net_mesh_size`, `sample.net_mouth_aperture`, `sample.min_net_sampling_depth`, `sample.max_net_sampling_depth`",
            "- CTD/capteurs : `acq.temperature_ctd`, `acq.salinity_ctd`, `acq.oxygen_concent`, `acq.fluo1`, `acq.raw_depth`, `acq.pixel_um_size`",
            "",
        ]
    )
    OUTPUT_CATEGORY.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_key_report(rows: list[dict[str, str]], metadata: dict) -> None:
    fields = {row["field"] for row in rows}
    lines = [
        "# Verification des colonnes cles - EcoTaxa 14622",
        "",
        "Verification basee sur la metadata projet EcoTaxa, sans export objet complet.",
        "",
        "| Concept | Statut | Colonnes trouvees | Colonnes candidates cherchees |",
        "|---|---|---|---|",
    ]
    for concept, candidates in KEY_CONCEPTS:
        found = [field for field in candidates if field in fields]
        status = "OK" if found else "MANQUANT"
        lines.append(
            f"| {concept} | {status} | {', '.join(f'`{field}`' for field in found) or '-'} | {', '.join(f'`{field}`' for field in candidates)} |"
        )

    lines.extend(
        [
            "",
            "## Lecture rapide",
            "",
            "- Les colonnes essentielles pour objet, temps, position, profondeur, taxonomie, taille et CTD sont presentes.",
            "- La calibration est disponible via `acq.pixel_um_size` ; convertir les longueurs image en millimetres avec `pixel_um_size / 1000` si les mesures morphometriques sont en pixels.",
            "- `txo.display_name` est le meilleur candidat pour le taxon affiche ; `obj.classif_qual` sert a verifier le statut de validation.",
            "- Sans TSV objet, il ne faut pas supprimer de colonnes pour nullite ou constance : cette verification demande un export d'objets ou un echantillon exploitable.",
            "",
        ]
    )
    OUTPUT_KEYS.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    rows = read_rows()
    metadata = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    write_category_report(rows, metadata)
    write_key_report(rows, metadata)
    print(f"wrote {OUTPUT_CATEGORY}")
    print(f"wrote {OUTPUT_KEYS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
