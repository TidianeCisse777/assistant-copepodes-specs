import pytest
from polar_data_tools import joins


class TestPlan:
    def test_plan_identifies_join_key(self, ecotaxa_1165_tsv, ecopart_105_tsv):
        pytest.fail("not implemented")

    def test_plan_does_not_execute_join(self, ecotaxa_1165_tsv, ecopart_105_tsv):
        pytest.fail("not implemented")


class TestExecute:
    def test_execute_requires_validated_plan(self):
        pytest.fail("not implemented")

    def test_joined_table_has_columns_from_both_sources(self, ecotaxa_1165_tsv, ecopart_105_tsv):
        pytest.fail("not implemented")
