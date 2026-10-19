import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from condominiums.models import Block


@pytest.mark.django_db
class TestBlockModel:
    def test_str_shows_condominium_and_name(self, make_block):
        block = make_block(name="Bloco J")
        assert str(block) == f"{block.condominium} - Bloco J"

    def test_new_block_passes_full_clean(self, make_condominium):
        block = Block(condominium=make_condominium(), name="Bloco A")
        block.full_clean()  # must not raise

    def test_is_active_defaults_to_true(self, make_block):
        assert make_block().is_active is True

    # --- unique name per condominium (case-insensitive) -------------------

    def test_duplicate_name_in_same_condominium_fails_full_clean(self, make_block):
        existing = make_block(name="Bloco A")
        duplicate = Block(condominium=existing.condominium, name="Bloco A")

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "already exists in this condominium" in str(exc.value)

    def test_duplicate_name_ignores_case(self, make_block):
        existing = make_block(name="Bloco A")
        duplicate = Block(condominium=existing.condominium, name="bloco a")

        with pytest.raises(ValidationError):
            duplicate.full_clean()

    def test_same_name_in_other_condominium_is_allowed(
        self, make_block, make_condominium
    ):
        make_block(name="Bloco A")
        other = Block(condominium=make_condominium(), name="Bloco A")
        other.full_clean()  # must not raise

    def test_database_enforces_unique_name_even_without_full_clean(self, make_block):
        existing = make_block(name="Bloco A")

        with pytest.raises(IntegrityError), transaction.atomic():
            Block.objects.create(condominium=existing.condominium, name="BLOCO a")

    # --- condominium cannot change ---------------------------------------

    def test_changing_condominium_fails_with_error_on_the_field(
        self, make_block, make_condominium
    ):
        block = make_block()
        block.condominium = make_condominium()

        with pytest.raises(ValidationError) as exc:
            block.full_clean()

        assert "condominium" in exc.value.message_dict

    def test_editing_only_the_name_is_allowed(self, make_block):
        block = make_block(name="Bloco A")
        block.name = "Bloco B"
        block.full_clean()  # must not raise

    def test_creating_a_block_does_not_trigger_the_lock(self, make_condominium):
        # UUID pk exists before save(); _state.adding must be what decides.
        block = Block(condominium=make_condominium(), name="Bloco A")
        assert block.pk is not None
        block.full_clean()  # must not raise


@pytest.mark.django_db
class TestBlockManager:
    def test_stored_condominium_id_returns_saved_value(self, make_block):
        block = make_block()
        assert Block.objects.stored_condominium_id(block.pk) == block.condominium_id

    def test_stored_condominium_id_returns_none_for_unknown_pk(self):
        import uuid

        assert Block.objects.stored_condominium_id(uuid.uuid4()) is None

    def test_stored_condominium_id_ignores_unsaved_changes(
        self, make_block, make_condominium
    ):
        block = make_block()
        original = block.condominium_id
        block.condominium = make_condominium()  # in memory only

        assert Block.objects.stored_condominium_id(block.pk) == original
