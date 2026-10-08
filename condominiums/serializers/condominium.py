from django.db import transaction
from rest_framework import serializers

from condominiums.models import Condominium, CondominiumBilling
from condominiums.serializers.condominium_billing import CondominiumBillingSerializer
from setup.models import Address
from setup.serializers.address import AddressSerializer


class CondominiumSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    billing = CondominiumBillingSerializer()

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Condominium
        fields = (
            "id",
            "company",
            "billing",
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
        read_only_fields = ("company",)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop("address")
        billing_data = validated_data.pop("billing")

        address = Address.objects.create(**address_data)

        condominium = Condominium.objects.create(address=address, **validated_data)

        CondominiumBilling.objects.create(condominium=condominium, **billing_data)

        return condominium

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        billing_data = validated_data.pop("billing", None)

        if address_data:
            for field, value in address_data.items():
                setattr(instance.address, field, value)
            instance.address.save()

        if billing_data:
            for field, value in billing_data.items():
                setattr(instance.billing, field, value)
            instance.billing.save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        return instance
