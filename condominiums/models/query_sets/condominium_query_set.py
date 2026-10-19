from typing import TYPE_CHECKING
from uuid import UUID

from django.db import models

if TYPE_CHECKING:
    from condominiums.models import Condominium


class CondominiumQuerySet(models.QuerySet["Condominium"]):
    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.filter(pk=pk).values_list("company_id", flat=True).first()


class CondominiumManager(models.Manager["Condominium"]):
    def get_queryset(self) -> CondominiumQuerySet:
        return CondominiumQuerySet(self.model, using=self.db)

    def stored_company_id(self, pk: UUID) -> UUID | None:
        return self.get_queryset().stored_condominium_id(pk)
