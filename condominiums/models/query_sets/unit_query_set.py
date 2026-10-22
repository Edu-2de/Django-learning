from typing import TYPE_CHECKING
from uuid import UUID

from django.db import models

if TYPE_CHECKING:
    from condominiums.models import Unit


class UnitQuerySet(models.QuerySet["Unit"]):
    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.filter(pk=pk).values_list("condominium_id", flat=True).first()

    def stored_block_id(self, pk: UUID) -> UUID | None:
        return self.filter(pk=pk).values_list("block_id", flat=True).first()


class UnitManager(models.Manager["Unit"]):
    def get_queryset(self) -> UnitQuerySet:
        return UnitQuerySet(self.model, using=self.db)

    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.get_queryset().stored_condominium_id(pk)

    def stored_block_id(self, pk: UUID) -> UUID | None:
        return self.get_queryset().stored_block_id(pk)
