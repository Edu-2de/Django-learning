from rest_framework.routers import DefaultRouter

from condominiums.views import CompanyViewSet
from condominiums.views.block_view import BlockViewSet
from condominiums.views.condominium_view import CondominiumViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("condominiums", CondominiumViewSet, basename="condominium")
router.register("blocks", BlockViewSet, basename="block")


urlpatterns = router.urls
