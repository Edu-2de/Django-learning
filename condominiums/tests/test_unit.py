import pytest
from django.core.exceptions import ValidationError

from condominiums.models import Unit


@pytest.mark.django_db
class TestUnitModel:
    def test_create_instance(self, make_unit):
        unit = make_unit(name="Unit 01")
        assert str(unit) == f"{unit.condominium} - Unit 01"

    def test_duplicate_unit_in_same_block(self, make_unit):
        existing = make_unit(name="Unit 01")
        duplicate = Unit(
            condominium=existing.condominium, block=existing.block, name="Unit 01"
        )

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "This unit already exists in this block" in str(exc.value)

    def test_duplicate_unit_in_same_condominium(self, make_unit):
        existing = make_unit(name="Unit 01", block=None)
        duplicate = Unit(block=None, condominium=existing.condominium, name="Unit 01")

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "This unit already exists in this condominium" in str(exc.value)

    def test_ideal_fraction_around_zero_and_one(self):
        unit = Unit(name="Unit 01", ideal_fraction=2)

        with pytest.raises(ValidationError) as exc:
            unit.full_clean()

        assert "Unit ideal fraction must be between around 0 and 1" in str(exc.value)

    def test_amounts_grater_than_zero(self):
        unit = Unit(gas_amount=-1, water_amount=-1, electricity_amount=-1)

        with pytest.raises(ValidationError) as exc:
            unit.full_clean()

        assert "Unit amounts must be null or grater than 0" in str(exc.value)
