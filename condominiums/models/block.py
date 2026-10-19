from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.db.models.functions import Lower

from condominiums.models.query_sets import BlockManager
from setup.models import BaseModel

from .condominium import Condominium


class Block(BaseModel):
    condominium = models.ForeignKey(
        Condominium, on_delete=models.PROTECT, related_name="blocks"
    )
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    objects = BlockManager()

    class Meta(BaseModel.Meta):
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
        constraints = (
            models.UniqueConstraint(
                F("condominium"),
                Lower("name"),
                name="block_condominium_name_unique_lower",
                violation_error_message="A block with this name already exists in this condominium",
            ),
        )

    def __str__(self) -> str:
        return f"{self.condominium} - {self.name}"

    def clean(self):
        super().clean()

        if self._state.adding:
            return

        stored_id = Block.objects.stored_condominium_id(self.pk)

        if stored_id is not None and stored_id != self.condominium_id:
            raise ValidationError(
                {"condominium": "The condominium of a block cannot be changed."}
            )
