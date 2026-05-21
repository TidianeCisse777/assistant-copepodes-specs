import pytest
from polar_data_tools import columns


class TestDescribe:
    def test_known_column_returns_definition(self):
        pytest.fail("not implemented")

    def test_unknown_column_returns_not_found(self):
        pytest.fail("not implemented")


class TestCheckForCalculation:
    def test_missing_required_column_blocks_calc(self):
        pytest.fail("not implemented")

    def test_all_required_columns_present_allows_calc(self):
        pytest.fail("not implemented")
