from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values


PROJECT_ID = 14622
PROJECT_LABEL = "LOKI_ArcticNet_2015"
PROJECT_SLUG = "loki_arcticnet_2015"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
GREEN_EXPORT = REPO_ROOT / "data_exploration" / "ecotaxa_green_edge_probe" / "src" / "export_green_edge_authenticated.py"
FALLBACK_ENV = REPO_ROOT / "data_exploration" / "ecotaxa_green_edge_probe" / ".env"


def load_export_module():
    spec = importlib.util.spec_from_file_location("ecotaxa_green_edge_export", GREEN_EXPORT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load export module from {GREEN_EXPORT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_export_module()
    module.PROJECT_ID = PROJECT_ID
    module.PROJECT_LABEL = PROJECT_LABEL
    module.PROJECT_SLUG = PROJECT_SLUG
    module.ROOT = ROOT
    module.RAW = ROOT / "outputs" / "raw"
    module.REPORT = ROOT / "outputs" / "report.md"
    module.MAX_REQUESTS = 500

    def load_credentials(args):
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
            password = module.getpass.getpass("EcoTaxa password: ")
        return None, username, password

    module.load_credentials = load_credentials

    def inspect_if_zip(path: Path) -> None:
        if path.suffix.lower() == ".zip":
            subprocess.run([sys.executable, str(ROOT / "src" / "inspect_14622_export.py"), str(path)], check=False)

    module.inspect_if_zip = inspect_if_zip
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
