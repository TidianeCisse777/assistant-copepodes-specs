from __future__ import annotations

import csv
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


ECOTAXA_PROJECT_ID = 1165
EXPECTED_ECOPART_DATASET_ID = 105
ECOPART_BASE = "https://ecopart.obs-vlfr.fr"
ECOTAXA_BASE = "https://ecotaxa.obs-vlfr.fr"

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
RAW = OUTPUTS / "raw"
REPORT = OUTPUTS / "report_ecopart_link.md"

MAX_REQUESTS = 20
TIMEOUT = 60


ECOTAXA_FIELDS = [
    "obj.orig_id",
    "obj.depth_min",
    "obj.depth_max",
    "obj.objdate",
    "obj.objtime",
    "obj.latitude",
    "obj.longitude",
    "fre.area",
    "fre.major",
    "fre.minor",
    "fre.feret",
    "fre.esd",
    "fre.width",
    "fre.height",
    "txo.display_name",
]


@dataclass
class ProbeResult:
    request_count: int = 0
    ecotaxa_title: str | None = None
    ecotaxa_access: str | None = None
    ecotaxa_instrument: str | None = None
    ecotaxa_object_count: int | None = None
    ecotaxa_free_object_fields: list[str] = field(default_factory=list)
    ecotaxa_sample_fields: list[str] = field(default_factory=list)
    ecotaxa_query_columns: list[str] = field(default_factory=list)
    ecotaxa_query_total: int | None = None

    ecopart_home_accessible: bool = False
    ecopart_candidate_dataset_id: int | None = None
    ecopart_candidate_dataset_name: str | None = None
    ecopart_contains_1165_option: bool = False
    ecopart_samples_count: int | None = None
    ecopart_sample_ids: list[int] = field(default_factory=list)
    ecopart_sample_visibility: list[str] = field(default_factory=list)
    ecopart_popover_link_confirmed: bool = False
    ecopart_popover_text: str | None = None
    ecopart_stats_available: bool = False
    ctd_columns: list[str] = field(default_factory=list)
    reduced_particle_columns: list[str] = field(default_factory=list)
    detailed_particle_columns: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class RequestBudget:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.count = 0
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ecopart-1165-link-probe/0.1"})

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        if self.count >= self.limit:
            raise RuntimeError(f"request budget exceeded ({self.limit})")
        last_error: Exception | None = None
        for attempt in range(1, 4):
            try:
                self.count += 1
                return self.session.request(method, url, timeout=TIMEOUT, **kwargs)
            except requests.RequestException as exc:
                last_error = exc
                if attempt < 3:
                    time.sleep(2 * attempt)
        raise RuntimeError(f"request failed after retries: {method} {url}: {last_error}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def save_response(prefix: str, response: requests.Response) -> Path:
    content_type = response.headers.get("content-type", "")
    suffix = ".json" if "json" in content_type else ".html" if "html" in content_type else ".bin"
    path = RAW / f"{prefix}{suffix}"
    write_bytes(path, response.content)
    meta = {
        "url": response.url,
        "status_code": response.status_code,
        "content_type": content_type,
        "headers": dict(response.headers),
        "saved_as": str(path.relative_to(ROOT)),
    }
    write_text(RAW / f"{prefix}_meta.json", json.dumps(meta, indent=2, ensure_ascii=False))
    return path


def parse_select_options(soup: BeautifulSoup, select_id: str) -> list[dict[str, str]]:
    select = soup.find("select", id=select_id)
    if not select:
        return []
    options = []
    for option in select.find_all("option"):
        value = (option.get("value") or "").strip()
        label = option.get_text(" ", strip=True)
        if value:
            options.append({"value": value, "label": label})
    return options


def parse_ecopart_home(html: str, result: ProbeResult) -> None:
    soup = BeautifulSoup(html, "html.parser")
    dataset_options = parse_select_options(soup, "filt_uproj")
    write_text(RAW / "ecopart_dataset_options.json", json.dumps(dataset_options, indent=2, ensure_ascii=False))

    for option in dataset_options:
        if option["value"] == str(EXPECTED_ECOPART_DATASET_ID):
            result.ecopart_candidate_dataset_id = EXPECTED_ECOPART_DATASET_ID
            result.ecopart_candidate_dataset_name = option["label"]
        if option["value"] == str(ECOTAXA_PROJECT_ID):
            result.ecopart_contains_1165_option = True

    result.ctd_columns = [f"{o['value']} = {o['label']}" for o in parse_select_options(soup, "ctd")]
    result.reduced_particle_columns = [f"{o['value']} = {o['label']}" for o in parse_select_options(soup, "gpr")]
    result.detailed_particle_columns = [f"{o['value']} = {o['label']}" for o in parse_select_options(soup, "gpd")]


def parse_ecotaxa_project(data: dict[str, Any], result: ProbeResult) -> None:
    result.ecotaxa_title = data.get("title")
    result.ecotaxa_access = str(data.get("access"))
    result.ecotaxa_instrument = data.get("instrument")
    objcount = data.get("objcount")
    result.ecotaxa_object_count = int(objcount) if isinstance(objcount, (int, float)) else None
    result.ecotaxa_free_object_fields = sorted((data.get("obj_free_cols") or {}).keys())
    result.ecotaxa_sample_fields = sorted((data.get("sample_free_cols") or {}).keys())


def write_ecopart_samples(samples: list[dict[str, Any]]) -> None:
    if not samples:
        return
    with (RAW / "ecopart_105_samples.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(samples[0].keys()))
        writer.writeheader()
        writer.writerows(samples)


def write_ecotaxa_query_sample(data: dict[str, Any], fields: list[str]) -> list[str]:
    base_columns = ["object_id", "acquisition_id", "sample_id", "project_id"]
    detail_columns = [field.replace(".", "_") for field in fields]
    columns = base_columns + detail_columns
    rows = []
    object_ids = data.get("object_ids") or []
    acquisition_ids = data.get("acquisition_ids") or []
    sample_ids = data.get("sample_ids") or []
    project_ids = data.get("project_ids") or []
    details = data.get("details") or []
    count = min(len(object_ids), len(acquisition_ids), len(sample_ids), len(project_ids), len(details), 100)
    for idx in range(count):
        row = {
            "object_id": object_ids[idx],
            "acquisition_id": acquisition_ids[idx],
            "sample_id": sample_ids[idx],
            "project_id": project_ids[idx],
        }
        for col, value in zip(detail_columns, details[idx]):
            row[col] = value
        rows.append(row)
    if rows:
        with (RAW / "ecotaxa_1165_query_sample.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
    return columns


def strip_html(html: str) -> str:
    return re.sub(r"\s+", " ", BeautifulSoup(html, "html.parser").get_text(" ", strip=True)).strip()


def render_report(result: ProbeResult) -> str:
    link = result.ecopart_popover_link_confirmed
    direct = "oui" if link else "non"
    dataset_public = "oui" if result.ecopart_samples_count and result.ecopart_samples_count > 0 else "non"
    reliable_join = "oui" if link and result.ecotaxa_query_columns and result.ecopart_samples_count else "a verifier"
    lines = [
        "EcoPart / EcoTaxa link test — EcoTaxa project 1165",
        "",
        f"1. EcoTaxa project 1165 accessible ? {'oui' if result.ecotaxa_title else 'non'}",
        f"   - titre : {result.ecotaxa_title or 'inconnu'}",
        f"   - instrument : {result.ecotaxa_instrument or 'inconnu'}",
        f"   - objets : {result.ecotaxa_object_count if result.ecotaxa_object_count is not None else 'inconnu'}",
        f"2. Dataset EcoPart candidat trouve ? {'oui' if result.ecopart_candidate_dataset_id else 'non'}",
        f"   - dataset_id : {result.ecopart_candidate_dataset_id or 'inconnu'}",
        f"   - nom : {result.ecopart_candidate_dataset_name or 'inconnu'}",
        f"3. Liaison EcoPart -> EcoTaxa 1165 confirmee ? {direct}",
        "   - preuve : getsamplepopover mentionne 'Ecotaxa Project : UVP5 IPS Amundsen 2018 (1165)'"
        if link
        else "   - preuve : non trouvee",
        f"4. Dataset EcoPart public/visible ? {dataset_public}",
        f"   - samples visibles : {result.ecopart_samples_count if result.ecopart_samples_count is not None else 'inconnu'}",
        f"   - sample_ids : {', '.join(map(str, result.ecopart_sample_ids)) if result.ecopart_sample_ids else 'inconnu'}",
        "5. Colonnes / champs EcoTaxa utiles :",
    ]
    for column in result.ecotaxa_query_columns:
        lines.append(f"   - {column}")
    lines.extend(
        [
            "6. Champs morphometriques EcoTaxa declares :",
        ]
    )
    for field in result.ecotaxa_free_object_fields:
        lines.append(f"   - {field}")
    lines.extend(
        [
            "7. Champs sample EcoTaxa declares :",
        ]
    )
    for field in result.ecotaxa_sample_fields:
        lines.append(f"   - {field}")
    lines.extend(
        [
            "8. CTD visible dans EcoPart :",
        ]
    )
    for column in result.ctd_columns:
        lines.append(f"   - {column}")
    lines.extend(
        [
            "9. Particules visibles/exportables dans EcoPart :",
            f"   - histogramme reduit : {len(result.reduced_particle_columns)} variables",
            f"   - histogramme detaille : {len(result.detailed_particle_columns)} variables",
            "10. Export EcoPart :",
            "   - route detectee : /Task/Create/TaskPartExport",
            "   - non lancee dans ce probe pour eviter de creer un job; la visibilite YY indique donnees visibles/exportables",
            "11. Conclusion :",
            f"   - liaison directe possible ? {direct}",
            f"   - jointure fiable probable ? {reliable_join}",
            "   - EcoPart peut servir de source centrale UVP + CTD ? oui, pour ce dataset candidat",
            "   - EcoTaxa sert pour objets/taxonomie/morphometrie image ? oui",
            f"   - requetes effectuees : {result.request_count}/{MAX_REQUESTS}",
        ]
    )
    if result.ecopart_popover_text:
        lines.extend(["", "Preuve popover EcoPart :", f"- {result.ecopart_popover_text}"])
    if result.notes:
        lines.append("")
        lines.append("Notes :")
        lines.extend(f"- {note}" for note in result.notes)
    return "\n".join(lines) + "\n"


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    result = ProbeResult()
    budget = RequestBudget(MAX_REQUESTS)

    response = budget.request("GET", f"{ECOPART_BASE}/")
    result.request_count = budget.count
    save_response("ecopart_home", response)
    result.ecopart_home_accessible = response.ok
    if response.ok:
        parse_ecopart_home(response.text, result)

    response = budget.request("GET", f"{ECOPART_BASE}/searchsample", params={"filt_uproj": str(EXPECTED_ECOPART_DATASET_ID)})
    result.request_count = budget.count
    save_response("ecopart_105_searchsample", response)
    if response.ok:
        samples = response.json()
        result.ecopart_samples_count = len(samples)
        result.ecopart_sample_ids = [int(sample["id"]) for sample in samples if "id" in sample]
        result.ecopart_sample_visibility = [str(sample.get("visibility", "")) for sample in samples]
        write_ecopart_samples(samples)

    if result.ecopart_sample_ids:
        sample_id = result.ecopart_sample_ids[0]
        response = budget.request("GET", f"{ECOPART_BASE}/getsamplepopover/{sample_id}")
        result.request_count = budget.count
        save_response(f"ecopart_sample_{sample_id}_popover", response)
        if response.ok:
            text = strip_html(response.text)
            result.ecopart_popover_text = text
            result.ecopart_popover_link_confirmed = f"({ECOTAXA_PROJECT_ID})" in text and "Ecotaxa Project" in text

    response = budget.request("GET", f"{ECOPART_BASE}/statsample", params={"filt_uproj": str(EXPECTED_ECOPART_DATASET_ID)})
    result.request_count = budget.count
    save_response("ecopart_105_statsample", response)
    result.ecopart_stats_available = response.ok

    response = budget.request("GET", f"{ECOTAXA_BASE}/api/projects/{ECOTAXA_PROJECT_ID}")
    result.request_count = budget.count
    save_response("ecotaxa_1165_project_model", response)
    if response.ok:
        parse_ecotaxa_project(response.json(), result)

    response = budget.request(
        "POST",
        f"{ECOTAXA_BASE}/api/object_set/{ECOTAXA_PROJECT_ID}/query",
        params={"fields": ",".join(ECOTAXA_FIELDS), "window_start": 0, "window_size": 25},
        json={"statusfilter": "V"},
        headers={"Accept": "application/json"},
    )
    result.request_count = budget.count
    save_response("ecotaxa_1165_object_query", response)
    if response.ok:
        data = response.json()
        write_text("".join([]) or RAW / "ecotaxa_1165_object_query_pretty.json", json.dumps(data, indent=2, ensure_ascii=False))
        result.ecotaxa_query_total = data.get("total_ids")
        result.ecotaxa_query_columns = write_ecotaxa_query_sample(data, ECOTAXA_FIELDS)

    result.request_count = budget.count
    write_text(RAW / "run_summary.json", json.dumps(result.__dict__, indent=2, ensure_ascii=False))
    write_text(REPORT, render_report(result))
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
