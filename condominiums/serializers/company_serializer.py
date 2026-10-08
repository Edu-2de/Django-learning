from django.db import transaction
from rest_framework import serializers

from condominiums.models import Company
from setup.models import Address
from setup.serializers. import AddressSerializer


class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Company
        fields = (
            (
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
            ),
        )
        read_only_fields = ("is_active",)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop("address")

        address = Address.objects.create(**address_data)

        return Company.objects.create(address=address, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)

        if address_data:
            for field, value in address_data.items():
                setattr(instance.address, field, value)
            instance.address.save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        return instance
