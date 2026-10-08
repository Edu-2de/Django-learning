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

    def _current_value(self, attrs, field):
        if field in attrs:
            return attrs[field]
        billing = getattr(self.root.instance, "billing", None)
        return getattr(billing, field, None)

    def validate(self, attrs):
        percent = self._current_value(attrs, "early_payment_discount_percent")
        amount = self._current_value(attrs, "early_payment_discount_amount")
        days = self._current_value(attrs, "early_payment_discount_days")

        if percent is not None and amount is not None:
            raise serializers.ValidationError(
                "Provide either a discount percent or a discount amount, not both."
            )

        if (percent is not None or amount is not None) and days is None:
            raise serializers.ValidationError(
                {"early_payment_discount_days": ("Required when a discount is set.")}
            )

        return attrs
