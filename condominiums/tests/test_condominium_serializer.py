from types import SimpleNamespace

import pytest

from condominiums.serializers import CondominiumSerializer


def make_context(*, company_id=None, superuser=True, authenticated=True):
    """Fake request context. Replace with a real User once the User model exists."""
    user = SimpleNamespace(
        is_authenticated=authenticated,
        is_superuser=superuser,
        company_id=company_id,
    )
    return {"request": SimpleNamespace(user=user)}


@pytest.mark.django_db
class TestCondominiumSerializer:
    def test_valid_create(self, make_company, condominium_payload):
        serializer = CondominiumSerializer(
            data=condominium_payload(name="Sol"), context=make_context()
        )

        assert serializer.is_valid(), serializer.errors
        condominium = serializer.save(company=make_company())

        assert condominium.name == "Sol"
        assert condominium.billing.due_day == 10
