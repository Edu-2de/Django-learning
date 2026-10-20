from django.db import transaction
from rest_framework import serializers

from condominiums.models import Condominium, CondominiumBilling
from condominiums.serializers.block_serializer import BlockSerializer
from condominiums.serializers.condominium_billing_serializer import (
    CondominiumBillingSerializer,
)
from setup.models import Address
from setup.serializers import AddressSerializer


class CondominiumSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    billing = CondominiumBillingSerializer()
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Condominium
        fields = (
            "id",
            "company",
            "billing",
            "blocks",
            "code",
            "name",
            "type",
            "cnpj",
            "municipal_registration",
            "address",
            "water_meter_code",
            "electricity_meter_code",
            "administration_start_date",
            "is_active",
        )
        read_only_fields = ("company", "blocks")

    @transaction.atomic
    def create(self, validated_data):
        company = validated_data.pop("company")
        address_data = validated_data.pop("address")
        billing_data = validated_data.pop("billing")
        return Condominium.create_with_related(
            company=company,
            condominium_data=validated_data,
            address_data=address_data,
            billing_data=billing_data,
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        billing_data = validated_data.pop("billing", None)

        return instance.update_profile(
            condominium_data=validated_data,
            address_data=address_data,
            billing_data=billing_data,
        )
