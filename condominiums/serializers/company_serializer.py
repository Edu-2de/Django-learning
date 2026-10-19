import re

from rest_framework import serializers

from condominiums.models import Company
from setup.serializers import AddressSerializer


class CompanySerializer(serializers.ModelSerializer):
    DIGITS_ONLY_FIELDS = ("cnpj", "phone")

    address = AddressSerializer()

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Company
        fields = (
            "id",
            "legal_name",
            "trade_name",
            "cnpj",
            "municipal_registration",
            "creci",
            "email",
            "phone",
            "website",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("is_active",)

    def to_internal_value(self, data):
        data = data.copy()
        for name in self.DIGITS_ONLY_FIELDS:
            value = data.get(name)
            if isinstance(value, str):
                data[name] = re.sub(r"\D", "", value)
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)

        return instance.update_profile(
            company_data=validated_data,
            address_data=address_data,
        )
