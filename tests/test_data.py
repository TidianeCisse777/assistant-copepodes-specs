import pytest
from polar_data_tools import data


class TestInspect:
    def test_returns_shape_and_columns(self, ecotaxa_1165_tsv):
        pytest.fail("not implemented")

    def test_preview_has_5_rows(self, ecotaxa_1165_tsv):
        pytest.fail("not implemented")

    def test_raises_on_missing_file(self):
        pytest.fail("not implemented")


class TestValidate:
    def test_valid_tsv_returns_valid_true(self, ecotaxa_1165_tsv):
        pytest.fail("not implemented")

    def test_identifies_missing_required_columns(self, ecotaxa_1165_tsv):
        pytest.fail("not implemented")

    def test_raw_data_not_modified(self, ecotaxa_1165_tsv):
        pytest.fail("not implemented")


class TestProfileMissing:
    def test_returns_missing_counts_per_column(self, ecotaxa_1165_tsv):
        pytest.fail("not implemented")
