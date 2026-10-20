import pytest
from django.core.exceptions import ValidationError

from condominiums.models.condominium import Condominium


@pytest.mark.django_db
class TestCondominiumModel:
    def test_str_shows_code_and_name(self, make_condominium):
        condominium = make_condominium(name="Condo 01")
        assert str(condominium) == f"{condominium.code} - Condo 01"

    def test_duplicate_code_in_same_company(self, make_condominium):
        existing = make_condominium(code="0001")
        duplicate = Condominium(company=existing.company, code="0001")

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "This condominium already exists in this company" in str(exc.value)
