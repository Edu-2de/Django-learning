from django.db import models
from django.db.models.functions import Lower

from setup.models import Address
from setup.models.base import BaseModel
from setup.validators.cnpj import validate_cnpj


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
    website = models.CharField(max_length=200, blank=True)

    address = models.OneToOneField(
        Address, on_delete=models.PROTECT, related_name="companies"
    )

    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        constraints = models.UniqueConstraint(
            Lower("email"), name="company_email_unique_lower"
        )

    def __str__(self) -> str:
        return f"{self.trade_name}"
