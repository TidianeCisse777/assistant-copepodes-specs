import pytest
from polar_data_tools import sources


class TestListAvailable:
    def test_returns_list_of_known_sources(self):
        pytest.fail("not implemented")


class TestDescribe:
    def test_known_source_returns_metadata(self):
        pytest.fail("not implemented")

    def test_unknown_source_raises(self):
        pytest.fail("not implemented")


class TestQueryEcotaxa:
    def test_credentials_not_exposed_in_result(self):
        pytest.fail("not implemented")


class TestQueryObis:
    def test_absence_qualified_not_null(self):
        pytest.fail("not implemented")
