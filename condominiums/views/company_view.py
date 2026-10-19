from rest_framework import mixins, viewsets

from condominiums.models import Company
from condominiums.serializers.company_serializer import CompanySerializer


class CompanyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CompanySerializer
    http_method_names = (
        "get",
        "patch",
        "head",
        "options",
    )

    def get_queryset(self):
        queryset = Company.objects.select_related("address")

        user = self.request.user
        if user.is_superuser:
            return queryset

        return queryset.filter(pk=user.company_id)
