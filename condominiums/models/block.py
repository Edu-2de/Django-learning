from django.db import models
from django.db.models import F
from django.db.models.functions import Lower

from condominiums.models import Condominium
from setup.models import BaseModel


class Block(BaseModel):
    condominium = models.ForeignKey(
        Condominium, on_delete=models.PROTECT, related_name="blocks"
    )
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
        constraints = models.UniqueConstraint(
            F("condominium"),
            Lower("name"),
            name="block_condominium_name_unique_lower",
        )

    def __str__(self) -> str:
        return f"{self.condominium} - {self.name}"
