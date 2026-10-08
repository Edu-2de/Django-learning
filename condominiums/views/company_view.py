from rest_framework import mixins, viewsets

from condominiums.models import Company
from condominiums.serializers.company import CompanySerializer


class CompanyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.select_related("address").order_by("trade_name")

        user = self.request.user
        if user.is_superuser:
            return queryset

        return queryset.filter(pk=user.company_id)
