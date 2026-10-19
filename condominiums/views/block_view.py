from rest_framework import mixins, viewsets

from condominiums.models import Block
from condominiums.serializers import BlockSerializer


class BlockViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BlockSerializer
    http_method_names = (
        "post",
        "get",
        "patch",
        "head",
        "options",
    )

    def get_queryset(self):
        queryset = Block.objects.select_related("condominium").order_by(
            "condominium", "name"
        )

        user = self.request.user
        if user.is_superuser:
            return queryset

        return queryset.filter(condominium__company_id=user.company_id)
