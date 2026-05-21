import pytest
from polar_data_tools import context


class TestGetRequiredFields:
    def test_analyse_mode_requires_species_and_region(self):
        pytest.fail("not implemented")

    def test_exploration_mode_has_no_required_fields(self):
        pytest.fail("not implemented")


class TestValidateSpecies:
    def test_known_species_returns_valid(self):
        pytest.fail("not implemented")

    def test_ambiguous_species_returns_warning(self):
        pytest.fail("not implemented")

    def test_unknown_species_returns_invalid(self):
        pytest.fail("not implemented")
