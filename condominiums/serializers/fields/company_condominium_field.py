from rest_framework import serializers

from condominiums.models import Condominium


class CompanyCondominiumField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user is None or not user.is_authenticated:
            return Condominium.objects.none()

        if user.is_superuser:
            return Condominium.objects.all()

        return Condominium.objects.filter(company_id=user.company_id)
