from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.expressions import F
from django.db.models.functions import Lower
from django.db.models.query_utils import Q

from condominiums.models import Block, Condominium
from condominiums.models.query_sets import UnitManager
from setup.models.base import BaseModel


class Unit(BaseModel):
    class Type(models.TextChoices):
        APARTMENT = ("apartment", "Apartment")
        OFFICE = ("office", "Office")
        STORE = ("store", "Store")
        HOUSE = ("house", "House")
        COMMERCIAL_SUITE = ("commercial_suite", "Commercial Suite")
        PARKING_SPACE = ("parking_space", "Parkin Space")
        OTHER = ("other", "OTHER")

    condominium = models.ForeignKey(
        Condominium,
        on_delete=models.PROTECT,
        related_name="units",
    )
    condominium_id: UUID

    block = models.ForeignKey(
        Block,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="units"
    )
    block_id: UUID | None

    name = models.CharField(max_length=30)
    type = models.CharField(max_length=32, choices=Type.choices, default=Type.APARTMENT)

    resident_count = models.PositiveSmallIntegerField(default=0)
    ideal_fraction = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    is_syndic_unit = models.BooleanField(default=False)
    is_rented = models.BooleanField(default=False)

    property_registration = models.CharField(max_length=255, blank=True)

    gas_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    water_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    electricity_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    entries_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UnitManager()

    class Meta(BaseModel.Meta):
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        constraints = (
            models.UniqueConstraint(
                F("condominium"),
                F("block"),
                Lower("name"),
                condition=Q(block__isnull=False),
                name="unit_name_condominium_block_unique",
                violation_error_message="This unit already exists in this block",
            ),
            models.UniqueConstraint(
                F("condominium"),
                Lower("name"),
                condition=Q(block__isnull=True),
                name="unit_name_condominium_unique",
                violation_error_message="This unit already exists in this condominium",
            ),
            models.CheckConstraint(
                condition=(Q(ideal_fraction__lte=1) & Q(ideal_fraction__gte=0)),
                name="unit_ideal_fraction_due_range",
                violation_error_message="Unit ideal fraction must be between around 0 and 1",
            ),
            models.CheckConstraint(
                condition=(
                    (Q(gas_amount__gte=0) | Q(gas_amount__isnull=True))
                    & (Q(water_amount__gte=0) | Q(water_amount__isnull=True))
                    & (
                        Q(electricity_amount__gte=0)
                        | Q(electricity_amount__isnull=True)
                    )
                ),
                name="unit_amounts_null_or_grater_than_0",
                violation_error_message="Unit amounts must be null or grater than 0",
            ),
        )

    def __str__(self) -> str:
        return f"{self.condominium} - {self.name}"

    def clean(self):
        super().clean()

        if self.block_id and self.block.condominium_id != self.condominium_id:
            raise ValidationError(
                {"block": "The block does not belong to this condominium"}
            )

        if self._state.adding:
            return

        stored_condominium_id = Unit.objects.stored_condominium_id(self.pk)

        if (
            stored_condominium_id is not None
            and stored_condominium_id != self.condominium_id
        ):
            raise ValidationError(
                {"condominium": "The condominium of unit cannot be changed"}
            )
