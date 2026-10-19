from rest_framework.routers import DefaultRouter

from condominiums.views import CompanyViewSet
from condominiums.views.block_view import BlockViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("blocks", BlockViewSet, basename="block")


urlpatterns = router.urls
