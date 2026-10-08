from rest_framework import mixins, viewsets

from condominiums.models import Condominium
from condominiums.serializers.condominium_serializer import CondominiumSerializer


class CondominiumViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CondominiumSerializer

    def get_queryset(self):
        queryset = (
            Condominium.objects.select_related("address", "billing")
            .prefetch_related("blocks")
            .order_by("code")
        )

        user = self.request.user
        if user.is_superuser:
            return queryset

        return queryset.filter(company_id=user.company_id)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
