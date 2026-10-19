from rest_framework import serializers

from condominiums.models import Block
from condominiums.serializers.fields import (
    CompanyCondominiumField,
)
from condominiums.serializers.mixins import ModelCleanMixin


class BlockSerializer(ModelCleanMixin, serializers.ModelSerializer):
    condominium = CompanyCondominiumField()

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Block
        fields = ("id", "condominium", "name", "is_active")
