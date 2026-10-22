from rest_framework import serializers

from condominiums.models import Block


class CompanyBlockField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user is None or not user.is_authenticated:
            return Block.objects.none()

        if user.is_superuser:
            return Block.objects.all()

        return Block.objects.filter(condominium__company=user.company_id)
