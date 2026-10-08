from django.db import models
from typing_extensions import override

from setup.models.base import BaseModel
from setup.validators.cep import validate_cep


class Address(BaseModel):
    class StateChoices(models.TextChoices):
        AC = "AC", "Ac"
        AL = "AL", "Al"
        AP = "AP", "Ap"
        AM = "AM", "Am"
        BA = "BA", "Ba"
        CE = "CE", "Ce"
        DF = "DF", "Df"
        ES = "ES", "Es"
        GO = "GO", "Go"
        MA = "MA", "Ma"
        MT = "MT", "Mt"
        MS = "MS", "Ms"
        MG = "MG", "Mg"
        PA = "PA", "Pa"
        PB = "PB", "Pb"
        PR = "PR", "Pr"
        PE = "PE", "Pe"
        PI = "PI", "Pi"
        RJ = "RJ", "Rj"
        RN = "RN", "Rn"
        RS = "RS", "Rs"
        RO = "RO", "Ro"
        RR = "RR", "Rr"
        SC = "SC", "Sc"
        SP = "SP", "Sp"
        SE = "SE", "Se"
        TO = "TO", "To"

    zip_code = models.CharField(max_length=8, blank=True, validators=[validate_cep])
    street = models.CharField(
        max_length=254,
    )

    number = models.CharField(
        max_length=20,
        blank=True,
    )
    complement = models.CharField(
        max_length=254,
        blank=True,
    )
    neighborhood = models.CharField(
        max_length=254,
        blank=True,
    )

    city = models.CharField(
        max_length=254,
    )
    state = models.CharField(max_length=2, choices=StateChoices)

    class Meta(BaseModel.Meta):
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    @override
    def __str__(self) -> str:
        return f"{self.city} - {self.street} - {self.state}"
