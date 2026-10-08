from typing import TYPE_CHECKING

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.query_utils import Q

from setup.models.base import BaseModel

from .condominium import Condominium


class CondominiumBilling(BaseModel):
    if TYPE_CHECKING:

        def get_calculation_competence_display(self) -> str: ...

    class CalculationCompetence(models.TextChoices):
        REFERENCE_MONTH = ("reference_month", "Reference Month")
        FOLLOWING_MONTH = ("following_month", "Following Month")

    condominium = models.OneToOneField(
        Condominium, on_delete=models.CASCADE, related_name="billing"
    )

    due_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(28)],
    )
    due_on_business_day = models.BooleanField(default=True)
    calculation_competence = models.CharField(
        max_length=30,
        choices=CalculationCompetence.choices,
        default=CalculationCompetence.REFERENCE_MONTH,
    )

    early_payment_discount_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
    )
    early_payment_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    early_payment_discount_days = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(28)],
        blank=True,
        null=True,
    )
    credit_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Condominium Billing"
        verbose_name_plural = "Condominium Billings"
        constraints = (
            models.CheckConstraint(
                name="condominium_billing_due_day_range",
                condition=(Q(due_day__gte=1) & Q(due_day__lte=28)),
            ),
            models.CheckConstraint(
                name="condominium_billing_discount_percent_xor_amount",
                condition=Q(early_payment_discount_percent__isnull=True)
                | Q(early_payment_discount_amount__isnull=True),
            ),
            models.CheckConstraint(
                name="condominium_billing_discount_days_required",
                condition=(
                    Q(early_payment_discount_percent__isnull=True)
                    | Q(early_payment_discount_amount__isnull=True)
                    & Q(early_payment_discount_days__isnull=False)
                ),
            ),
        )

    def __str__(self) -> str:
        return f"{self.condominium} - {self.get_calculation_competence_display()}"
