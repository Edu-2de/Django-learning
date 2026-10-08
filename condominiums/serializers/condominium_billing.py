from rest_framework import serializers

from condominiums.models import CondominiumBilling


class CondominiumBillingSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = CondominiumBilling
        fields = (
            "due_day",
            "due_on_business_day",
            "calculation_competence",
            "early_payment_discount_percent",
            "early_payment_discount_amount",
            "early_payment_discount_days",
            "credit_limit",
        )
