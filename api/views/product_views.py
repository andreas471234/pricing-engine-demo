import logging
from services.utils import request_query_params_to_dict, request_pagination
from pricingapp.manager.product_manager import ProductManager
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="list")
    def product_list(self, request):
        page, page_size = request_pagination(request.query_params)
        query_params = request_query_params_to_dict(request.query_params)
        resp_data = ProductManager().get_product_list(query_params, page, page_size)

        return Response(status=HTTP_200_OK, data=resp_data)

    @action(methods=["post"], detail=False, url_path="add-product")
    def add_product(self, request):
        status, data = ProductManager().create(request.data)
        return Response(status=status, data=data)

    @action(methods=["post"], detail=False, url_path="add-product-unit")
    def add_product_unit(self, request):
        status, data = ProductManager().create_unit(request.data)
        return Response(status=status, data=data)
