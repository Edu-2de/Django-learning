from types import SimpleNamespace

import pytest

from condominiums.serializers import UnitSerializer


def make_context(*, company_id=None, superuser=True, authenticated=True):
    """Fake request context. Replace with a real User once the User model exists."""
    user = SimpleNamespace(
        is_authenticated=authenticated,
        is_superuser=superuser,
        company_id=company_id,
    )
    return {"request": SimpleNamespace(user=user)}


@pytest.mark.django_db
class TestUnitSerializer:
    def test_valid_create(self, make_condominium, make_block):
        condominium = make_condominium()
        block = make_block(condominium=condominium)
        serializer = UnitSerializer(
            data={"name": "Unit 01", "condominium": condominium.pk, "block": block.pk},
            context=make_context(),
        )

        assert serializer.is_valid(), serializer.errors
        unit = serializer.save()

        assert unit.name == "Unit 01"
