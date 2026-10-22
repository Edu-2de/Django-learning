from rest_framework import mixins, viewsets

from condominiums.models import Unit
from condominiums.serializers.unit_serializer import UnitSerializer


class UnitViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UnitSerializer
    http_method_name = ("post", "get", "patch", "head", "options")

    def get_queryset(self):
        queryset = Unit.objects.prefetch_related("condominium").order_by("name")

        user = self.request.user
        if user.is_superuser:
            return queryset

        return queryset.filter(company_id=user.company_id)

    def perform_create(self, serializer):
        return serializer.save(company=self.request.user.company)
