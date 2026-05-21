from pathlib import Path
import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def ecotaxa_1165_tsv() -> Path:
    return FIXTURES_DIR / "uvp_amundsen_1165_ecotaxa_object_sample.tsv"


@pytest.fixture
def ecopart_105_tsv() -> Path:
    return FIXTURES_DIR / "uvp_amundsen_105_ecopart_particles_reduced.tsv"


@pytest.fixture
def enriched_join_tsv() -> Path:
    return FIXTURES_DIR / "uvp_amundsen_1165_105_enriched_nearest_depth.tsv"


@pytest.fixture
def amundsen_ctd_tsv() -> Path:
    return FIXTURES_DIR / "amundsen_12713_ctd_2018_sample.tsv"


@pytest.fixture
def loki_ecotaxa_tsv() -> Path:
    return FIXTURES_DIR / "loki_2331_ecotaxa_export_sample_50.tsv"
