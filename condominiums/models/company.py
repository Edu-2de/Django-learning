from django.db import models, transaction
from django.db.models.functions import Lower
from django.db.models.query_utils import Q

from setup.models import Address
from setup.models.base import BaseModel
from setup.validators.cnpj import validate_cnpj
from setup.validators.model_clean import full_clean_all


class Company(BaseModel):
    legal_name = models.CharField(
        max_length=254,
    )
    trade_name = models.CharField(max_length=254)

    cnpj = models.CharField(max_length=14, unique=True, validators=[validate_cnpj])

    municipal_registration = models.CharField(max_length=50, blank=True)

    creci = models.CharField(max_length=20, blank=True)

    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=17, blank=True)
    website = models.URLField(max_length=200, blank=True)

    address = models.OneToOneField(Address, on_delete=models.PROTECT)

    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        constraints = (
            models.UniqueConstraint(
                Lower("email"),
                name="company_email_unique_lower",
                violation_error_message="This email is already in use",
            ),
            models.CheckConstraint(
                name="company_cnpj_has_14_digits",
                condition=Q(cnpj__regex=r"^[0-9]{14}$"),
                violation_error_message="CNPJ must contain exactly 14 digits",
            ),
        )

    def __str__(self) -> str:
        return f"{self.trade_name}"

    @transaction.atomic
    def update_profile(self, *, company_data=None, address_data=None):
        company_data = company_data or {}
        address_data = address_data or {}

        for field, value in address_data.items():
            setattr(self.address, field, value)

        for field, value in company_data.items():
            setattr(self, field, value)

        full_clean_all({"": self, "address": self.address})

        self.address.save()
        self.save()

        return self
