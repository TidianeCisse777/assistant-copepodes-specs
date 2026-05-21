from __future__ import annotations

import io
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
REPORT = ROOT / "outputs" / "report.md"
MAX_BYTES = 2_000_000
SAMPLE_BYTES = 200_000

KEY_PATTERNS = {
    "cast_id": re.compile(r"cast|profile", re.I),
    "event_id": re.compile(r"event", re.I),
    "station": re.compile(r"station|site", re.I),
    "date_time": re.compile(r"date|time|yyyy", re.I),
    "lat/lon": re.compile(r"lat|lon|longitude|latitude", re.I),
    "depth": re.compile(r"depth|pressure", re.I),
}
ENV_PATTERNS = {
    "temperature": re.compile(r"temp|temperature|TE90", re.I),
    "salinity/conductivity": re.compile(r"salin|conduct|PSAL", re.I),
    "oxygen": re.compile(r"oxygen|dissolved|OXYM", re.I),
    "fluorescence": re.compile(r"fluor|chloro|chlorophyll|FLOR", re.I),
}


def load_json(name: str) -> Any:
    return json.loads((RAW / name).read_text(encoding="utf-8"))


def sanitize_name(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", text).strip("_")[:120]


def is_probably_csv(url: str, resource: dict[str, Any], content_type: str | None) -> bool:
    text = f"{url} {resource.get('format')} {resource.get('name')} {content_type}".lower()
    return any(token in text for token in [".csv", "csv", "text/plain", "erddap"])


def erddap_csv_url(url: str) -> str | None:
    if url.startswith("http://erddap."):
        url = "https://" + url[len("http://") :]
    if "erddap" not in url.lower():
        return None
    if "/tabledap/" in url:
        base = url.split("?")[0]
        dataset_id = base.rstrip("/").split("/")[-1]
        dataset_id = re.sub(r"\.(html|graph|csv|json|nc|csvp)$", "", dataset_id)
        return build_erddap_sample_url(url, dataset_id)
    return None


def erddap_info(url: str, dataset_id: str) -> dict[str, Any]:
    parsed = urlparse(url.replace("http://erddap.", "https://erddap."))
    root = f"{parsed.scheme}://{parsed.netloc}/erddap"
    info_url = f"{root}/info/{dataset_id}/index.csv"
    response = requests.get(info_url, timeout=30)
    response.raise_for_status()
    info_path = RAW / f"erddap_info_{dataset_id}.csv"
    info_path.write_text(response.text, encoding="utf-8", errors="replace")
    df = pd.read_csv(io.StringIO(response.text))
    variables = df[df["Row Type"] == "variable"]["Variable Name"].dropna().astype(str).tolist()
    units = {}
    for _, row in df[df["Attribute Name"] == "units"].iterrows():
        units[str(row["Variable Name"])] = row["Value"]
    return {"info_url": info_url, "info_path": str(info_path.relative_to(ROOT)), "variables": variables, "units": units}


def build_erddap_sample_url(url: str, dataset_id: str) -> str:
    normalized = url.replace("http://erddap.", "https://erddap.")
    parsed = urlparse(normalized)
    root = f"{parsed.scheme}://{parsed.netloc}/erddap"
    info = erddap_info(normalized, dataset_id)
    variables = info["variables"]
    wanted = [
        "platform_name",
        "platform_id",
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
        "GPS",
        "Speed",
    ]
    selected = [var for var in wanted if var in variables]
    if not selected:
        selected = variables[:20]
    constraints = ""
    if "time" in variables:
        constraints = "&time>=2018-01-01T00:00:00Z&time<=2018-12-31T23:59:59Z"
    return f"{root}/tabledap/{dataset_id}.csvp?{','.join(selected)}{constraints}"


def read_csv_sample(url: str, resource_name: str) -> dict[str, Any]:
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    content = response.raw.read(SAMPLE_BYTES, decode_content=True)
    sample_path = RAW / f"sample_{sanitize_name(resource_name)}.csv"
    sample_path.write_bytes(content)

    text = content.decode("utf-8", errors="replace")
    preview_lines = text.splitlines()[:20]
    try:
        df = pd.read_csv(io.StringIO(text), sep=None, engine="python", nrows=20)
        columns = list(map(str, df.columns))
    except Exception as exc:
        columns = []
        preview_lines.append(f"CSV_PARSE_ERROR: {exc}")

    result = {
        "kind": "csv",
        "sample_path": str(sample_path.relative_to(ROOT)),
        "columns": columns,
        "preview_lines": preview_lines,
    }
    if "erddap" in url.lower() and "/tabledap/" in url:
        dataset_id = re.search(r"/tabledap/([^.?/]+)", url)
        if dataset_id:
            result["erddap_info"] = erddap_info(url, dataset_id.group(1))
    return result


def inspect_html_for_links(url: str, resource_name: str) -> dict[str, Any]:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    html_path = RAW / f"page_{sanitize_name(resource_name)}.html"
    html_path.write_text(response.text, encoding="utf-8", errors="replace")
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if any(ext in href.lower() for ext in [".csv", ".json", ".nc", "tabledap"]):
            links.append(href)
    return {
        "kind": "html",
        "sample_path": str(html_path.relative_to(ROOT)),
        "links": links[:20],
    }


def inspect_resource(dataset: dict[str, Any], resource: dict[str, Any]) -> dict[str, Any]:
    url = resource.get("url") or ""
    http = resource.get("http") or {}
    content_type = http.get("content_type")
    content_length = http.get("content_length")
    final_url = str(http.get("final_url") or url)
    if final_url.startswith("http://erddap."):
        final_url = "https://" + final_url[len("http://") :]
    name = f"{dataset.get('name')}_{resource.get('name') or resource.get('id')}"

    result = {
        "resource_name": resource.get("name"),
        "format": resource.get("format"),
        "url": url,
        "final_url": final_url,
        "content_type": content_type,
        "content_length": content_length,
        "inspected": False,
        "inspection": None,
    }

    try:
        size = int(content_length) if content_length else None
    except ValueError:
        size = None

    csv_url = erddap_csv_url(final_url) or final_url
    if size is not None and size > MAX_BYTES and not erddap_csv_url(final_url):
        result["skip_reason"] = f"too large for probe ({size} bytes)"
        return result

    try:
        if is_probably_csv(csv_url, resource, str(content_type)):
            result["inspection"] = read_csv_sample(csv_url, name)
            result["inspected"] = True
        elif "html" in str(content_type).lower() or final_url.endswith("/"):
            result["inspection"] = inspect_html_for_links(final_url, name)
            result["inspected"] = True
        else:
            result["skip_reason"] = "unsupported or non-tabular resource for small probe"
    except Exception as exc:
        result["error"] = str(exc)
    return result


def detect_presence(names: list[str], patterns: dict[str, re.Pattern[str]]) -> dict[str, bool]:
    return {
        key: any(pattern.search(name) for name in names)
        for key, pattern in patterns.items()
    }


def write_report(datasets: list[dict[str, Any]], inspections: list[dict[str, Any]]) -> None:
    all_columns: dict[str, list[str]] = {}
    formats: dict[str, list[str]] = {}
    access: dict[str, str] = {}

    for dataset, inspected in zip(datasets, inspections):
        title = dataset.get("title") or dataset.get("name")
        formats[title] = sorted(
            {str(r.get("format") or "").strip() or "unknown" for r in dataset.get("resources", [])}
        )
        resources = dataset.get("resources", [])
        resource_text = " ".join(
            f"{resource.get('name', '')} {resource.get('format', '')} {resource.get('url', '')}"
            for resource in resources
        ).lower()
        if "forms.gle" in resource_text or "docs.google.com/forms" in resource_text or "demande" in resource_text:
            access[title] = "on-demand / request form"
        elif "erddap" in resource_text:
            access[title] = "direct via ERDDAP"
        else:
            access[title] = "direct/resource present" if resources else "no resource listed"
        for resource in inspected.get("resources", []):
            inspection = resource.get("inspection") or {}
            columns = inspection.get("columns") or []
            if columns:
                all_columns[f"{title} / {resource.get('resource_name')}"] = columns

    flat_columns = [column for cols in all_columns.values() for column in cols]
    keys = detect_presence(flat_columns, KEY_PATTERNS)
    env = detect_presence(flat_columns, ENV_PATTERNS)

    lines = [
        "# Amundsen Science data probe",
        "",
        "## 1. Datasets trouves",
    ]
    for dataset in datasets:
        title = dataset.get("title") or dataset.get("name")
        lines.extend(
            [
                f"- {title}",
                f"  - id/name: `{dataset.get('name')}`",
                f"  - license: {dataset.get('license_title') or dataset.get('license_id') or 'inconnu'}",
            ]
        )

    lines.extend(["", "## 2. Acces et formats"])
    for title in formats:
        lines.append(f"- {title}: {access[title]}, formats: {', '.join(formats[title])}")

    lines.extend(["", "## 3. Colonnes/variables detectees"])
    if all_columns:
        for label, columns in all_columns.items():
            lines.append(f"- {label}")
            for column in columns[:80]:
                lines.append(f"  - `{column}`")
            if len(columns) > 80:
                lines.append(f"  - ... {len(columns) - 80} colonnes supplementaires")
    else:
        lines.append("- Aucune table lisible detectee dans les petits echantillons.")

    lines.extend(["", "## 4. Cles de liaison disponibles"])
    for key, present in keys.items():
        lines.append(f"- {key}: {'oui' if present else 'non'}")

    lines.extend(["", "## 5. Variables environnementales disponibles"])
    for key, present in env.items():
        lines.append(f"- {key}: {'oui' if present else 'non'}")

    lines.extend(
        [
            "",
            "## 6. Conclusion V1",
            f"- CTD-Rosette exploitable pour V1 ? {'oui' if any(env.values()) and keys.get('depth') else 'inconnu/non confirme'}",
            "- Scientific Event Log exploitable ? a confirmer ; Amundsen l'indique comme on-demand pour 2003-2020.",
            "- Navigation GPS exploitable ? utile seulement si les lat/lon des fichiers CTD/EcoPart ne suffisent pas.",
            "",
            "## 7. Limites",
            "- Probe volontairement limite a 3 datasets et 1 petit fichier par dataset.",
            "- Si les ressources pointent vers ERDDAP, le pipeline final devra construire des URLs de sous-selection propres.",
            "- Si une ressource est trop lourde, ce probe conserve seulement les metadonnees HTTP.",
        ]
    )

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    datasets = load_json("selected_datasets.json")
    resource_inspections = load_json("resources_inspection.json")

    file_inspections = []
    for dataset, inspected in zip(datasets, resource_inspections):
        dataset_result = {
            "id": dataset.get("id"),
            "name": dataset.get("name"),
            "title": dataset.get("title"),
            "resources": [],
        }
        inspected_one = False
        for resource in inspected.get("resources", []):
            result = inspect_resource(dataset, resource)
            if result.get("inspected"):
                inspected_one = True
            dataset_result["resources"].append(result)
            if inspected_one:
                break
        file_inspections.append(dataset_result)

    (RAW / "file_inspections.json").write_text(
        json.dumps(file_inspections, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_report(datasets, file_inspections)
    print(f"Saved report to {REPORT}")


if __name__ == "__main__":
    main()
