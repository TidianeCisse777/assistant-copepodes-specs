from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "outputs" / "raw"
REPORT = ROOT / "outputs" / "report_ecopart_export.md"
ECOPART_BASE = "https://ecopart.obs-vlfr.fr"
ENV_PATH = ROOT.parent / "ecotaxa_loki_probe" / ".env"


class Session:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ecopart-105-auth-export/0.1"})

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        last = None
        for attempt in range(1, 4):
            try:
                return self.session.request(method, url, timeout=60, **kwargs)
            except requests.RequestException as exc:
                last = exc
                time.sleep(2 * attempt)
        raise RuntimeError(f"{method} {url} failed after retries: {last}")


def login(client: Session) -> bool:
    load_dotenv(ENV_PATH)
    email = os.getenv("ECOTAXA_USERNAME")
    password = os.getenv("ECOTAXA_PASSWORD")
    if not email or not password:
        raise RuntimeError(f"missing credentials in {ENV_PATH}")
    response = client.request("POST", f"{ECOPART_BASE}/login", data={"email": email, "password": password}, allow_redirects=False)
    return response.status_code in {200, 302} and bool(response.cookies or response.headers.get("set-cookie"))


def export_params() -> list[tuple[str, str]]:
    return [
        ("filt_uproj", "105"),
        ("ctd", "temperature"),
        ("ctd", "practical_salinity"),
        ("ctd", "oxygen_mass"),
        ("ctd", "oxygen_vol"),
        ("ctd", "depth"),
        ("ctd", "datetime"),
        ("gpr", "cl6"),
        ("gpr", "cl7"),
        ("gpr", "cl8"),
        ("gpr", "bv6"),
        ("gpr", "bv7"),
        ("gpr", "bv8"),
        ("XScale", "I"),
        ("TimeScale", "R"),
    ]


def save_response(name: str, response: requests.Response) -> Path:
    ctype = response.headers.get("content-type", "").lower()
    suffix = ".html" if "html" in ctype else ".zip" if "zip" in ctype else ".tsv" if "tab" in ctype else ".csv" if "csv" in ctype else ".bin"
    path = RAW / f"{name}{suffix}"
    path.write_bytes(response.content)
    return path


def extract_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href:
            links.append(href)
    for match in re.findall(r"""(?:href|url|window\.location)\s*[:=]\s*['"]([^'"]+)""", html):
        links.append(match)
    return sorted(set(links))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--poll", type=int, default=8)
    parser.add_argument("--sleep", type=int, default=5)
    args = parser.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    client = Session()
    logged = login(client)
    if not logged:
        raise RuntimeError("EcoPart login failed")

    start = client.request("GET", f"{ECOPART_BASE}/Task/Create/TaskPartExport", params=export_params())
    start_path = save_response("ecopart_105_auth_export_start", start)
    links = extract_links(start.text) if "html" in start.headers.get("content-type", "").lower() else []

    candidates = [link for link in links if any(token in link.lower() for token in ["download", "file", "task", "zip", "csv", "tsv"])]
    downloaded: list[Path] = []
    checked: list[str] = []

    for _ in range(args.poll):
        for link in candidates:
            url = urljoin(ECOPART_BASE, link)
            if url in checked:
                continue
            checked.append(url)
            response = client.request("GET", url, allow_redirects=True)
            ctype = response.headers.get("content-type", "").lower()
            if response.ok and ("zip" in ctype or "csv" in ctype or "tab-separated" in ctype or response.content[:4] == b"PK\x03\x04"):
                downloaded.append(save_response("ecopart_105_auth_export_file", response))
        if downloaded:
            break
        time.sleep(args.sleep)

    (RAW / "ecopart_105_auth_export_links.txt").write_text("\n".join(links) + "\n", encoding="utf-8")
    lines = [
        "EcoPart 105 authenticated export attempt",
        "",
        f"1. Login EcoPart ? {'oui' if logged else 'non'}",
        f"2. Page export HTTP : {start.status_code}",
        f"3. Page export sauvegardee : {start_path.relative_to(ROOT)}",
        f"4. Liens detectes : {len(links)}",
        f"5. Fichiers telecharges : {len(downloaded)}",
    ]
    lines.extend(f"   - {path.relative_to(ROOT)}" for path in downloaded)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
