from rest_framework import serializers

from condominiums.models import Unit
from condominiums.serializers.fields import CompanyCondominiumField
from condominiums.serializers.fields.company_block_field import CompanyBlockField
from condominiums.serializers.mixins.model_clean_mixin import ModelCleanMixin


class UnitSerializer(ModelCleanMixin, serializers.ModelSerializer):
    condominium = CompanyCondominiumField()
    block = CompanyBlockField()
        
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Unit
        fields = (
            "id",
            "condominium",
            "block",
            "name",
            "type",
            "resident_count",
            "ideal_fraction",
            "is_syndic_unit",
            "is_rented",
            "property_registration",
            "gas_amount",
            "water_amount",
            "electricity_amount",
            "entries_blocked",
            "is_active",
        )
