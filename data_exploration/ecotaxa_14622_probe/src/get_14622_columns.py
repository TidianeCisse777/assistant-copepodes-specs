from __future__ import annotations

import argparse
import csv
import getpass
import json
from pathlib import Path
from typing import Any

import requests
from dotenv import dotenv_values


PROJECT_ID = 14622
PROJECT_LABEL = "LOKI_ArcticNet_2015"
BASE_URL = "https://ecotaxa.obs-vlfr.fr"
API_BASE = f"{BASE_URL}/api"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
FALLBACK_ENV = REPO_ROOT / "data_exploration" / "ecotaxa_green_edge_probe" / ".env"
OUTPUTS = ROOT / "outputs" / "sample"
TIMEOUT = 60

STANDARD_OBJECT_FIELDS = [
    ("object", "obj.orig_id", "Identifiant original de l'objet"),
    ("object", "obj.latitude", "Latitude de l'objet"),
    ("object", "obj.longitude", "Longitude de l'objet"),
    ("object", "obj.objdate", "Date de l'objet"),
    ("object", "obj.objtime", "Heure de l'objet"),
    ("object", "obj.depth_min", "Profondeur minimale"),
    ("object", "obj.depth_max", "Profondeur maximale"),
    ("object", "obj.classif_qual", "Statut de classification"),
    ("object", "obj.classif_id", "Identifiant taxonomique retenu"),
    ("object", "obj.classif_who", "Validateur ou classificateur"),
    ("object", "obj.classif_when", "Date de classification"),
    ("object", "obj.classif_auto_id", "Identifiant taxonomique automatique"),
    ("object", "obj.classif_auto_score", "Score de classification automatique"),
    ("object", "obj.classif_auto_when", "Date de classification automatique"),
    ("object", "obj.complement_info", "Information complementaire objet"),
    ("object", "obj.object_link", "Lien objet"),
    ("object", "obj.random_value", "Valeur aleatoire interne"),
    ("object", "obj.sunpos", "Position solaire calculee"),
    ("taxonomy", "txo.display_name", "Nom taxonomique affiche"),
    ("taxonomy", "txo.name", "Nom taxonomique brut"),
    ("taxonomy", "txo.id", "Identifiant taxonomique EcoTaxa"),
    ("taxonomy", "txo.parent_id", "Identifiant du parent taxonomique"),
    ("taxonomy", "txo.aphia_id", "Identifiant Aphia/WoRMS si disponible"),
]


def load_credentials(args: argparse.Namespace) -> tuple[str | None, str | None, str | None]:
    env_path = ROOT / ".env"
    values = dotenv_values(env_path if env_path.exists() else FALLBACK_ENV)
    token = args.token or values.get("ECOTAXA_TOKEN") or None
    username = args.username or values.get("ECOTAXA_USERNAME") or None
    password = values.get("ECOTAXA_PASSWORD") or None

    if token:
        return token.strip(), None, None
    if not username:
        username = input("EcoTaxa email: ").strip()
    if not password:
        password = getpass.getpass("EcoTaxa password: ")
    return None, username, password


def authenticate(session: requests.Session, args: argparse.Namespace) -> None:
    token, username, password = load_credentials(args)
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
        return
    if not username or not password:
        raise RuntimeError("missing EcoTaxa credentials")

    response = session.post(f"{API_BASE}/login", json={"username": username, "password": password}, timeout=TIMEOUT)
    if not response.ok:
        raise RuntimeError(f"login failed: HTTP {response.status_code} {response.text[:200]}")
    jwt = response.json()
    if not isinstance(jwt, str) or not jwt:
        raise RuntimeError("login response did not contain a JWT string")
    session.headers["Authorization"] = f"Bearer {jwt}"


def parse_classiffieldlist(value: str | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not value:
        return rows
    for raw_line in value.splitlines():
        line = raw_line.strip()
        if not line or "=" not in line:
            continue
        source_name, display_name = line.split("=", 1)
        source_name = source_name.strip()
        display_name = display_name.strip()
        rows.append(
            {
                "category": "classification_display",
                "field": f"fre.{source_name}",
                "source_name": source_name,
                "storage_slot": "",
                "display_name": display_name,
                "definition": f"Champ libre objet affiche dans la liste de classification sous le libelle {display_name}.",
            }
        )
    return rows


def mapping_rows(category: str, prefix: str, mapping: dict[str, str] | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not mapping:
        return rows
    for source_name, storage_slot in sorted(mapping.items(), key=lambda item: (item[1], item[0])):
        rows.append(
            {
                "category": category,
                "field": f"{prefix}.{source_name}",
                "source_name": source_name,
                "storage_slot": storage_slot,
                "display_name": source_name.replace("_", " "),
                "definition": f"Champ libre {category} fourni par EcoTaxa, stocke dans {storage_slot}.",
            }
        )
    return rows


def build_columns(project: dict[str, Any]) -> dict[str, Any]:
    standard_rows = [
        {
            "category": category,
            "field": field,
            "source_name": field.split(".", 1)[1],
            "storage_slot": "",
            "display_name": label,
            "definition": label,
        }
        for category, field, label in STANDARD_OBJECT_FIELDS
    ]
    free_object_rows = mapping_rows("object_free", "fre", project.get("obj_free_cols"))
    sample_rows = mapping_rows("sample", "sample", project.get("sample_free_cols"))
    acquisition_rows = mapping_rows("acquisition", "acq", project.get("acquisition_free_cols"))
    process_rows = mapping_rows("process", "process", project.get("process_free_cols"))
    classification_rows = parse_classiffieldlist(project.get("classiffieldlist"))

    return {
        "project": {
            "project_id": project.get("projid", PROJECT_ID),
            "title": project.get("title", PROJECT_LABEL),
            "instrument": project.get("instrument"),
            "object_count": project.get("objcount"),
            "pct_validated": project.get("pctvalidated"),
            "pct_classified": project.get("pctclassified"),
        },
        "counts": {
            "standard": len(standard_rows),
            "classification_display": len(classification_rows),
            "object_free": len(free_object_rows),
            "sample": len(sample_rows),
            "acquisition": len(acquisition_rows),
            "process": len(process_rows),
        },
        "columns": standard_rows + classification_rows + free_object_rows + sample_rows + acquisition_rows + process_rows,
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["category", "field", "source_name", "storage_slot", "display_name", "definition"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, payload: dict[str, Any]) -> None:
    project = payload["project"]
    counts = payload["counts"]
    columns = payload["columns"]
    by_category: dict[str, list[dict[str, str]]] = {}
    for row in columns:
        by_category.setdefault(row["category"], []).append(row)

    lines = [
        "# Colonnes EcoTaxa - projet 14622",
        "",
        "Extraction metadata-only : aucune ligne objet n'est telechargee.",
        "",
        "## Projet",
        "",
        f"- Projet : {project['title']} (`{project['project_id']}`)",
        f"- Instrument : {project['instrument']}",
        f"- Objets annonces : {project['object_count']}",
        f"- Pourcentage valide : {project['pct_validated']}",
        f"- Pourcentage classifie : {project['pct_classified']}",
        "",
        "## Comptes de colonnes",
        "",
    ]
    for category, count in counts.items():
        lines.append(f"- {category} : {count}")

    lines.extend(["", "## Colonnes par categorie", ""])
    for category in ["classification_display", "object", "taxonomy", "object_free", "sample", "acquisition", "process"]:
        rows = by_category.get(category, [])
        if not rows:
            continue
        lines.extend([f"### {category}", "", "| Champ | Slot | Libelle | Definition |", "|---|---:|---|---|"])
        for row in rows:
            lines.append(
                f"| `{row['field']}` | {row['storage_slot']} | {row['display_name']} | {row['definition']} |"
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch EcoTaxa project 14622 column metadata without object export.")
    parser.add_argument("--username", help="EcoTaxa email. If omitted, uses .env or prompts.")
    parser.add_argument("--token", help="EcoTaxa JWT token. Prefer username/password in .env for this workflow.")
    parser.add_argument("--use-cache", action="store_true", help="Use local raw project metadata if present.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    raw_metadata = OUTPUTS / "project_14622_metadata.json"

    if args.use_cache and raw_metadata.exists():
        project = json.loads(raw_metadata.read_text(encoding="utf-8"))
    else:
        session = requests.Session()
        session.headers.update({"User-Agent": "ecotaxa-14622-columns/0.1", "Accept": "application/json"})
        authenticate(session, args)
        response = session.get(f"{API_BASE}/projects/{PROJECT_ID}", timeout=TIMEOUT)
        if not response.ok:
            raise RuntimeError(f"project metadata failed: HTTP {response.status_code} {response.text[:300]}")
        project = response.json()
        write_json(raw_metadata, project)

    payload = build_columns(project)
    write_json(OUTPUTS / "columns_metadata.json", payload)
    write_tsv(OUTPUTS / "columns_metadata.tsv", payload["columns"])
    write_report(OUTPUTS / "columns_metadata_report.md", payload)
    print(f"wrote {OUTPUTS / 'columns_metadata_report.md'}")
    print(f"columns: {len(payload['columns'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
