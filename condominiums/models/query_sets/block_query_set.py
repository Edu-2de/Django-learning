from typing import TYPE_CHECKING
from uuid import UUID

from django.db import models

if TYPE_CHECKING:
    from condominiums.models import Block


class BlockQuerySet(models.QuerySet["Block"]):
    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.filter(pk=pk).values_list("condominium_id", flat=True).first()


class BlockManager(models.Manager["Block"]):
    def get_queryset(self) -> BlockQuerySet:
        return BlockQuerySet(self.model, using=self._db)

    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.get_queryset().stored_condominium_id(pk)
