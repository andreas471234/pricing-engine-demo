from django.urls import re_path, include
from api.views import customer_views
from rest_framework import routers

from api.views import (
    customer_views,
    supplier_views,
    product_views,
    quote_views,
    fleet_views,
)


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        self.trailing_slash = "/?"
        super(routers.SimpleRouter, self).__init__()


api_router = OptionalSlashRouter()

api_router.register(r"customer", customer_views.CustomerViewSet, basename="customer")
api_router.register(r"supplier", supplier_views.SupplierViewSet, basename="supplier")
api_router.register(r"product", product_views.ProductViewSet, basename="product")
api_router.register(r"quote", quote_views.QuoteViewSet, basename="quote")
api_router.register(r"fleet", fleet_views.FleetViewSet, basename="fleet")

urlpatterns = [
    re_path(r"", include((api_router.urls, "pricingapp"), namespace="pricingapp-api")),
]
