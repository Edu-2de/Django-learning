from typing import TYPE_CHECKING
from uuid import UUID

from django.db import models

if TYPE_CHECKING:
    from condominiums.models import CondominiumBilling


class CondominiumBillingQuerySet(models.QuerySet["CondominiumBilling"]):
    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.filter(pk=pk).values_list("condominium_id", flat=True).first()


class CondominiumBillingManager(models.Manager["CondominiumBilling"]):
    def get_queryset(self) -> CondominiumBillingQuerySet:
        return CondominiumBillingQuerySet(self.model, using=self.db)

    def stored_condominium_id(self, pk: UUID) -> UUID | None:
        return self.get_queryset().stored_condominium_id(pk)
