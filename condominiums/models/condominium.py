from django.db import models
from django.db.models.query_utils import Q

from setup.models import Address, BaseModel
from setup.validators.cnpj import validate_cnpj

from .company import Company


class Condominium(BaseModel):
    class Type(models.TextChoices):
        RESIDENTIAL = ("residential", "Residential")
        COMMERCIAL = ("commercial", "Commercial")

    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="condominiums"
    )
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

    class Meta(BaseModel.Meta):
        verbose_name = "Condominium"
        verbose_name_plural = "Condominiums"
        constraints = (
            models.UniqueConstraint(
                fields=("company", "code"), name="condominium_company_code_unique"
            ),
            models.UniqueConstraint(
                fields=("cnpj",), condition=Q(cnpj=""), name="condominium_cnpj_unique"
            ),
        )

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
