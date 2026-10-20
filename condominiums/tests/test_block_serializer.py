from types import SimpleNamespace

import pytest

from condominiums.serializers import BlockSerializer


def make_context(*, company_id=None, superuser=True, authenticated=True):
    """Fake request context. Replace with a real User once the User model exists."""
    user = SimpleNamespace(
        is_authenticated=authenticated,
        is_superuser=superuser,
        company_id=company_id,
    )
    return {"request": SimpleNamespace(user=user)}


@pytest.mark.django_db
class TestBlockSerializer:
    def test_valid_create(self, make_condominium):
        condominium = make_condominium()
        serializer = BlockSerializer(
            data={"condominium": condominium.pk, "name": "Bloco A"},
            context=make_context(),
        )

        assert serializer.is_valid(), serializer.errors
        block = serializer.save()

        assert block.name == "Bloco A"
        assert block.condominium == condominium

    def test_duplicate_name_is_rejected_ignoring_case(self, make_block):
        existing = make_block(name="Bloco A")
        serializer = BlockSerializer(
            data={"condominium": existing.condominium_id, "name": "bloco a"},
            context=make_context(),
        )

        assert not serializer.is_valid()
        assert "already exists" in str(serializer.errors)

    def test_same_name_in_another_condominium_is_allowed(
        self, make_block, make_condominium
    ):
        make_block(name="Bloco A")
        other = make_condominium()
        serializer = BlockSerializer(
            data={"condominium": other.pk, "name": "Bloco A"},
            context=make_context(),
        )

        assert serializer.is_valid(), serializer.errors

    def test_changing_condominium_is_rejected_on_the_field(
        self, make_block, make_condominium
    ):
        block = make_block()
        other = make_condominium()
        serializer = BlockSerializer(
            block,
            data={"condominium": other.pk},
            partial=True,
            context=make_context(),
        )

        assert not serializer.is_valid()
        assert "condominium" in serializer.errors

    def test_editing_only_the_name_is_allowed(self, make_block):
        block = make_block(name="Bloco A")
        serializer = BlockSerializer(
            block, data={"name": "Bloco B"}, partial=True, context=make_context()
        )

        assert serializer.is_valid(), serializer.errors
        assert serializer.save().name == "Bloco B"

    def test_condominium_of_another_company_is_rejected(
        self, make_condominium, make_company
    ):
        foreign_condominium = make_condominium()
        my_company = make_company()
        serializer = BlockSerializer(
            data={"condominium": foreign_condominium.pk, "name": "Bloco A"},
            context=make_context(company_id=my_company.pk, superuser=False),
        )

        assert not serializer.is_valid()
        assert "condominium" in serializer.errors

    def test_condominium_of_own_company_is_accepted(self, make_condominium):
        condominium = make_condominium()
        serializer = BlockSerializer(
            data={"condominium": condominium.pk, "name": "Bloco A"},
            context=make_context(company_id=condominium.company_id, superuser=False),
        )

        assert serializer.is_valid(), serializer.errors

    def test_anonymous_user_cannot_pick_any_condominium(self, make_condominium):
        condominium = make_condominium()
        serializer = BlockSerializer(
            data={"condominium": condominium.pk, "name": "Bloco A"},
            context=make_context(authenticated=False),
        )

        assert not serializer.is_valid()
        assert "condominium" in serializer.errors

    def test_missing_name_is_rejected(self, make_condominium):
        serializer = BlockSerializer(
            data={"condominium": make_condominium().pk}, context=make_context()
        )

        assert not serializer.is_valid()
        assert "name" in serializer.errors
