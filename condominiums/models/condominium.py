from typing import TYPE_CHECKING
from uuid import UUID

from django.db import models, transaction
from django.db.models.query_utils import Q
from rest_framework.exceptions import ValidationError

from condominiums.models.query_sets import CondominiumManager
from setup.models import Address, BaseModel
from setup.validators.cnpj import validate_cnpj
from setup.validators.model_clean import full_clean_all

from .company import Company


class Condominium(BaseModel):
    if TYPE_CHECKING:
        from .condominium_billing import CondominiumBilling

    class Type(models.TextChoices):
        RESIDENTIAL = ("residential", "Residential")
        COMMERCIAL = ("commercial", "Commercial")

    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="condominiums"
    )
    company_id: UUID
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    type = models.CharField(max_length=32, choices=Type.choices)
    cnpj = models.CharField(max_length=14, validators=[validate_cnpj], blank=True)
    municipal_registration = models.CharField(max_length=50, blank=True)

    address = models.OneToOneField(
        Address, on_delete=models.PROTECT, related_name="condominium"
    )

    water_meter_code = models.CharField(max_length=25, blank=True)
    electricity_meter_code = models.CharField(max_length=25, blank=True)
    administration_start_date = models.DateField()

    is_active = models.BooleanField(default=True)

    billing: "CondominiumBilling"

    objects = CondominiumManager()

    class Meta(BaseModel.Meta):
        verbose_name = "Condominium"
        verbose_name_plural = "Condominiums"
        constraints = (
            models.UniqueConstraint(
                fields=("company", "code"),
                name="condominium_company_code_unique",
                violation_error_message="This condominium already exists in this company",
            ),
            models.UniqueConstraint(
                fields=("company", "cnpj"),
                condition=~Q(cnpj=""),
                name="condominium_company_cnpj_unique",
                violation_error_message="This cnpj is already in use",
            ),
            models.CheckConstraint(
                name="condominium_cnpj_has_14_digits",
                condition=Q(cnpj="") | Q(cnpj__regex=r"^[0-9]{14}$"),
                violation_error_message="CNPJ must contain exactly 14 digits",
            ),
        )

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    def clean(self):
        super().clean()

        if self._state.adding:
            return

        stored_id = Condominium.objects.stored_company_id(self.pk)

        if stored_id is not None and stored_id != self.company_id:
            raise ValidationError(
                {"company": "The company of a condominium cannot be changed."}
            )

    @transaction.atomic
    def update_profile(self, *, address_data=None, billing_data=None):
        address_data = address_data or {}
        billing_data = billing_data or {}

        for field, value in address_data.items():
            setattr(self.address, field, value)

        for field, value in billing_data.items():
            setattr(self.billing, field, value)

        full_clean_all({"": self, "address": self.address, "billing": self.billing})
        self.address.save()
        self.billing.save()
        self.save()

        return self

    @classmethod
    @transaction.atomic
    def create_with_related(
        cls, *, company, condominium_data, address_data, billing_data
    ):
        from .condominium_billing import CondominiumBilling

        address = Address(**address_data)
        condominium = cls(company=company, address=address, **condominium_data)
        billing = CondominiumBilling(condominium=condominium, **billing_data)

        full_clean_all(
            {"": condominium, "address": address, "billing": billing},
            exclude={"": ["address"], "billing": ["condominium"]},
        )

        address.save()
        condominium.save()
        billing.save()

        return condominium
