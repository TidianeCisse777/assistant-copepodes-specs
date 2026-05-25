from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


PROJECT_ID = 14622
PROJECT_LABEL = "LOKI_ArcticNet_2015"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
GREEN_INSPECT = REPO_ROOT / "data_exploration" / "ecotaxa_green_edge_probe" / "src" / "inspect_green_edge_export.py"


def load_inspect_module():
    spec = importlib.util.spec_from_file_location("ecotaxa_green_edge_inspect", GREEN_INSPECT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load inspect module from {GREEN_INSPECT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    module = load_inspect_module()
    module.PROJECT_ID = PROJECT_ID
    module.PROJECT_LABEL = PROJECT_LABEL
    module.ROOT = ROOT
    module.OUTPUTS = ROOT / "outputs"
    module.RAW = module.OUTPUTS / "raw"
    module.REPORT = module.OUTPUTS / "report.md"
    module.DEFAULT_EXPORT = module.RAW / "ecotaxa_loki_arcticnet_2015_14622_export.zip"
    rc = module.main(argv)
    if rc == 0:
        subprocess.run([sys.executable, str(ROOT / "src" / "profile_14622_export.py")], check=False)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
