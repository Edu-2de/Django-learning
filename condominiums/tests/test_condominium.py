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

    def test_duplicate_cnpj_in_same_company(self, make_condominium):
        existing = make_condominium(cnpj="02074032000167")
        duplicate = Condominium(company=existing.company, cnpj="02074032000167")

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "This cnpj is already in use" in str(exc.value)

    def test_minum_length_of_cnpj(self, make_condominium):
        condominium = make_condominium()
        condominium.cnpj = "000"

        with pytest.raises(ValidationError) as exc:
            condominium.full_clean()

        assert "CNPJ must have 14 characters, without punctuation." in str(exc.value)

    def test_changing_company_fails(self, make_condominium, make_company):
        condominium = make_condominium()
        condominium.company = make_company()

        with pytest.raises(ValidationError) as exc:
            condominium.full_clean()

        assert "company" in exc.value.message_dict

    def test_editing_only_the_address_is_allowed(self, make_condominium, make_address):
        condominium = make_condominium()
        condominium.address = make_address()

        condominium.full_clean()

    def test_editing_only_the_billing_is_allowed(self, make_condominium, make_billing):
        condominium = make_condominium()
        condominium.billing = make_billing()

        condominium.full_clean()

    def test_edit_condominium_data_is_allowed(self, make_condominium):
        condominium = make_condominium()
        condominium.name = "Condo 002"

        condominium.full_clean()

    