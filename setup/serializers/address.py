from rest_framework import serializers

from setup.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Address
        fields = (
            "zip_code",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "state",
        )
