from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
DATASETS_PATH = RAW / "selected_datasets.json"


def inspect_url(url: str) -> dict[str, object]:
    if url.startswith("http://erddap."):
        url = "https://" + url[len("http://") :]
    info: dict[str, object] = {"url": url, "host": urlparse(url).netloc}
    try:
        response = requests.head(url, allow_redirects=True, timeout=30)
        info.update(
            {
                "head_status": response.status_code,
                "final_url": response.url,
                "content_type": response.headers.get("content-type"),
                "content_length": response.headers.get("content-length"),
            }
        )
        if response.status_code in {405, 403}:
            raise requests.HTTPError(f"HEAD returned {response.status_code}")
    except Exception as exc:
        info["head_error"] = str(exc)
        try:
            response = requests.get(url, stream=True, timeout=30)
            info.update(
                {
                    "get_status": response.status_code,
                    "final_url": response.url,
                    "content_type": response.headers.get("content-type"),
                    "content_length": response.headers.get("content-length"),
                }
            )
            response.close()
        except Exception as get_exc:
            info["get_error"] = str(get_exc)
    return info


def main() -> None:
    datasets = json.loads(DATASETS_PATH.read_text(encoding="utf-8"))
    inspected = []
    for dataset in datasets:
        item = {
            "id": dataset.get("id"),
            "name": dataset.get("name"),
            "title": dataset.get("title"),
            "resources": [],
        }
        for resource in dataset.get("resources", []):
            resource_info = dict(resource)
            url = resource.get("url")
            if url:
                resource_info["http"] = inspect_url(url)
            item["resources"].append(resource_info)
        inspected.append(item)

    out = RAW / "resources_inspection.json"
    out.write_text(json.dumps(inspected, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved resource inspection to {out}")


if __name__ == "__main__":
    main()
