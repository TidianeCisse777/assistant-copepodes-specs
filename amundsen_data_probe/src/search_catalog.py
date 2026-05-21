from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

CKAN = "https://catalogue.amundsenscience.com/api/3/action"
QUERIES = [
    "CTD Rosette Amundsen 2018",
    "CTD Rosette",
    "Données CTD recueillies par le NGCC Amundsen",
    "Scientific Event Log",
    "journal evenement",
    "journal scientifique",
    "Navigation GPS",
    "Amundsen 2018",
    "Amundsen CTD",
]

TARGET_DATASETS = [
    "ca-cioos_ccin-12713",  # CTD collected by CCGS Amundsen
    "ca-cioos_ccin-13248",  # Scientific stations / event log
    "ca-cioos_ccin-12447",  # Navigation GPS
]


def ckan_get(action: str, params: dict[str, Any]) -> dict[str, Any]:
    url = f"{CKAN}/{action}"
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN action failed: {action} {payload}")
    return payload["result"]


def dataset_score(dataset: dict[str, Any]) -> tuple[int, str]:
    text = " ".join(
        str(dataset.get(k, "")) for k in ("title", "name", "notes", "tags")
    ).lower()
    score = 0
    if "ctd" in text:
        score += 100
    if "rosette" in text:
        score += 80
    if "2018" in text:
        score += 50
    if "event" in text:
        score += 40
    if "navigation" in text or "gps" in text:
        score += 30
    if "erddap" in text:
        score += 20
    return score, str(dataset.get("title") or dataset.get("name") or "")


def compact_dataset(dataset: dict[str, Any]) -> dict[str, Any]:
    resources = []
    for resource in dataset.get("resources", []):
        resources.append(
            {
                "id": resource.get("id"),
                "name": resource.get("name"),
                "description": resource.get("description"),
                "format": resource.get("format"),
                "mimetype": resource.get("mimetype"),
                "url": resource.get("url"),
                "resource_type": resource.get("resource_type"),
            }
        )

    extras = {item.get("key"): item.get("value") for item in dataset.get("extras", [])}
    return {
        "id": dataset.get("id"),
        "name": dataset.get("name"),
        "title": dataset.get("title"),
        "notes": dataset.get("notes"),
        "license_title": dataset.get("license_title"),
        "license_id": dataset.get("license_id"),
        "doi": dataset.get("doi") or extras.get("citation identifier") or extras.get("doi"),
        "metadata_created": dataset.get("metadata_created"),
        "metadata_modified": dataset.get("metadata_modified"),
        "extras": extras,
        "resources": resources,
    }


def main() -> None:
    all_hits: dict[str, dict[str, Any]] = {}
    search_payloads: dict[str, Any] = {}

    for query in QUERIES:
        result = ckan_get("package_search", {"q": query, "rows": 8})
        search_payloads[query] = result
        for dataset in result.get("results", []):
            all_hits[dataset["id"]] = dataset

    selected: list[dict[str, Any]] = []
    for dataset_id in TARGET_DATASETS:
        try:
            detailed = ckan_get("package_show", {"id": dataset_id})
            selected.append(compact_dataset(detailed))
        except Exception as exc:
            print(f"Could not fetch target dataset {dataset_id}: {exc}")

    if len(selected) < 3:
        ranked = sorted(all_hits.values(), key=dataset_score, reverse=True)
        already = {dataset["id"] for dataset in selected}
        for dataset in ranked:
            if dataset["id"] in already:
                continue
            detailed = ckan_get("package_show", {"id": dataset["id"]})
            selected.append(compact_dataset(detailed))
            if len(selected) == 3:
                break

    (RAW / "catalog_search_results.json").write_text(
        json.dumps(search_payloads, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (RAW / "selected_datasets.json").write_text(
        json.dumps(selected, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved {len(selected)} selected datasets to {RAW / 'selected_datasets.json'}")
    for dataset in selected:
        print(f"- {dataset['title']} ({dataset['name']})")


if __name__ == "__main__":
    main()
