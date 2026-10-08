from rest_framework import serializers

from condominiums.models import Block
from condominiums.serializers.fields import (
    CompanyCondominiumField,
)


class BlockSerializer(serializers.ModelSerializer):
    condominium = CompanyCondominiumField()

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Block
        fields = ("id", "condominium", "name", "is_active")

    def validate_condominium(self, value):
        if self.instance is not None and value != self.instance.condominium:
            raise serializers.ValidationError(
                "The condominium of a block cannot be changed"
            )
        return value
