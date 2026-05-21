from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import requests
from requests import RequestException
from dotenv import load_dotenv


PROJECT_ID = 2331
BASE_URL = "https://ecotaxa.obs-vlfr.fr"
API_BASE = f"{BASE_URL}/api"
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
REPORT = ROOT / "outputs" / "report.md"
MAX_REQUESTS = 25
TIMEOUT = 60


class RequestBudget:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.count = 0
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "ecotaxa-loki-auth-export/0.1",
                "Accept": "application/json, application/zip, text/tab-separated-values, text/csv, */*",
            }
        )

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        if self.count >= self.limit:
            raise RuntimeError(f"request budget exceeded ({self.limit})")
        last_error: RequestException | None = None
        for attempt in range(1, 4):
            try:
                self.count += 1
                return self.session.request(method, url, timeout=TIMEOUT, **kwargs)
            except RequestException as exc:
                last_error = exc
                if attempt == 3:
                    break
                time.sleep(2 * attempt)
        raise RuntimeError(f"request failed after retries: {method} {url}: {last_error}")


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def save_response(prefix: str, response: requests.Response, save_body: bool = True) -> Path | None:
    meta = {
        "url": response.url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content_type": response.headers.get("content-type", ""),
        "request_count_hint": prefix,
    }
    write_text(RAW / f"{prefix}_meta.json", json.dumps(meta, indent=2, ensure_ascii=False))
    if not save_body:
        return None
    content_type = response.headers.get("content-type", "").lower()
    suffix = ".json" if "json" in content_type else ".zip" if "zip" in content_type else ".tsv" if "tab-separated" in content_type else ".bin"
    path = RAW / f"{prefix}{suffix}"
    write_bytes(path, response.content)
    return path


def load_credentials(args: argparse.Namespace) -> tuple[str | None, str | None, str | None]:
    load_dotenv(ROOT / ".env")
    token = args.token or os.getenv("ECOTAXA_TOKEN") or None
    username = args.username or os.getenv("ECOTAXA_USERNAME") or None
    password = os.getenv("ECOTAXA_PASSWORD") or None

    if token:
        return token.strip(), None, None

    if not username:
        username = input("EcoTaxa email: ").strip()
    if not password:
        password = getpass.getpass("EcoTaxa password: ")
    return None, username, password


def authenticate(budget: RequestBudget, args: argparse.Namespace) -> None:
    token, username, password = load_credentials(args)
    if token:
        budget.session.headers["Authorization"] = f"Bearer {token}"
        return
    if not username or not password:
        raise RuntimeError("missing EcoTaxa credentials")

    response = budget.request("POST", f"{API_BASE}/login", json={"username": username, "password": password})
    save_response("authenticated_login", response, save_body=False)
    if not response.ok:
        raise RuntimeError(f"login failed: HTTP {response.status_code} {response.text[:200]}")
    jwt = response.json()
    if not isinstance(jwt, str) or not jwt:
        raise RuntimeError("login response did not contain a JWT string")
    budget.session.headers["Authorization"] = f"Bearer {jwt}"


def start_export(budget: RequestBudget, with_images: str, statusfilter: str) -> int:
    payload = {
        "filters": {"statusfilter": statusfilter},
        "request": {
            "project_id": PROJECT_ID,
            "split_by": "none",
            "with_images": with_images,
            "with_internal_ids": True,
            "with_types_row": False,
            "only_annotations": False,
            "out_to_ftp": False,
        },
    }
    response = budget.request("POST", f"{API_BASE}/object_set/export/general", json=payload)
    save_response("authenticated_export_start", response)
    if not response.ok:
        raise RuntimeError(f"export start failed: HTTP {response.status_code} {response.text[:300]}")
    data = response.json()
    job_id = data.get("job_id") if isinstance(data, dict) else None
    if not isinstance(job_id, int) or job_id <= 0:
        raise RuntimeError(f"export did not return a usable job_id: {data}")
    return job_id


def wait_for_job(budget: RequestBudget, job_id: int, poll_seconds: int, max_polls: int) -> dict[str, Any]:
    last_job: dict[str, Any] = {}
    for poll_idx in range(1, max_polls + 1):
        response = budget.request("GET", f"{API_BASE}/jobs/{job_id}/")
        save_response(f"authenticated_export_job_{job_id}_poll_{poll_idx}", response)
        if not response.ok:
            raise RuntimeError(f"job poll failed: HTTP {response.status_code} {response.text[:300]}")
        last_job = response.json()
        state = last_job.get("state")
        if state == "F":
            return last_job
        if state in {"E", "A"}:
            raise RuntimeError(f"job stopped in state {state}: {json.dumps(last_job, ensure_ascii=False)[:800]}")
        time.sleep(poll_seconds)
    raise RuntimeError(f"job {job_id} did not finish after {max_polls} polls; last={last_job}")


def download_job_file(budget: RequestBudget, job_id: int) -> Path:
    response = budget.request("GET", f"{API_BASE}/jobs/{job_id}/file")
    save_response(f"authenticated_export_job_{job_id}_file_response", response, save_body=False)
    if not response.ok:
        raise RuntimeError(f"job file download failed: HTTP {response.status_code} {response.text[:300]}")

    content_type = response.headers.get("content-type", "").lower()
    if response.content[:4] == b"PK\x03\x04" or "zip" in content_type:
        path = RAW / f"ecotaxa_loki_2331_export_job_{job_id}.zip"
    elif "tab-separated" in content_type:
        path = RAW / f"ecotaxa_loki_2331_export_job_{job_id}.tsv"
    elif "csv" in content_type:
        path = RAW / f"ecotaxa_loki_2331_export_job_{job_id}.csv"
    else:
        path = RAW / f"ecotaxa_loki_2331_export_job_{job_id}.bin"
    write_bytes(path, response.content)
    return path


def inspect_if_zip(path: Path) -> None:
    if path.suffix.lower() == ".zip":
        subprocess.run([sys.executable, str(ROOT / "src" / "inspect_loki_export.py"), str(path)], check=False)


def write_auth_report(job_id: int, job: dict[str, Any], file_path: Path, request_count: int) -> None:
    lines = [
        "EcoTaxa LOKI authenticated export — project 2331",
        "",
        "1. Authentification EcoTaxa ? oui",
        "2. Export officiel lance ? oui",
        f"3. Job ID : {job_id}",
        f"4. Etat final du job : {job.get('state')}",
        f"5. Fichier telecharge : {file_path.relative_to(ROOT)}",
        f"6. Requetes effectuees : {request_count}/{MAX_REQUESTS}",
        "",
        "Conclusion :",
        "- export ZIP/CSV/TSV officiel obtenu avec compte si le fichier ci-dessus est lisible.",
    ]
    write_text(REPORT, "\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Authenticated EcoTaxa export for LOKI project 2331.")
    parser.add_argument("--username", help="EcoTaxa email. If omitted, uses .env or prompts.")
    parser.add_argument("--token", help="EcoTaxa JWT token. Prefer env var ECOTAXA_TOKEN.")
    parser.add_argument("--with-images", choices=["none", "first", "all"], default="none")
    parser.add_argument("--statusfilter", default="V", help="Default V means validated objects.")
    parser.add_argument("--poll-seconds", type=int, default=5)
    parser.add_argument("--max-polls", type=int, default=12)
    parser.add_argument("--job-id", type=int, help="Resume an already-started export job.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    budget = RequestBudget(MAX_REQUESTS)
    authenticate(budget, args)
    job_id = args.job_id or start_export(budget, args.with_images, args.statusfilter)
    job = wait_for_job(budget, job_id, args.poll_seconds, args.max_polls)
    file_path = download_job_file(budget, job_id)
    inspect_if_zip(file_path)
    write_auth_report(job_id, job, file_path, budget.count)
    print(f"Downloaded {file_path}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
