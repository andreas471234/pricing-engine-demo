import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from pricingapp.manager.supplier_manager import SupplierManager
from pricingapp.models.product import Product
from pricingapp.models.supplier import Supplier
from services.utils import request_pagination, request_query_params_to_dict

logger = logging.getLogger(__name__)


class SupplierViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="list")
    def supplier_list(self, request):
        page, page_size = request_pagination(request.query_params)
        query_params = request_query_params_to_dict(request.query_params)
        resp_data = SupplierManager().get_supplier_list(query_params, page, page_size)

        return Response(status=HTTP_200_OK, data=resp_data)

    @action(methods=["get"], detail=True, url_path="detail")
    def supplier_detail(self, _, pk):
        supplier_obj = get_object_or_404(Supplier, id=pk)
        status, supplier_data = SupplierManager(supplier_obj).get_detail()

        return Response(status=status, data=supplier_data)

    @action(methods=["post"], detail=False, url_path="add-supplier")
    def add_supplier(self, request):
        status, data = SupplierManager().create(request.data)
        return Response(status=status, data=data)

    @action(methods=["post"], detail=True, url_path="add-products")
    def add_supplier_products(self, request, pk):
        supplier_obj = get_object_or_404(Supplier, id=pk)
        product_code = request.data.get("product_code")
        product_obj = Product.objects.filter(code=product_code)
        if not product_obj.exists():
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "err_message": f"product_code {product_code} is wrong or doesn't exist"
                },
            )
        try:
            status, data = SupplierManager(supplier_obj).add_products(
                product_obj.first(), request.data
            )
        except ObjectDoesNotExist:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"err_message": "Unit given doesn't exists"},
            )
        except Exception as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={"err_message": f"{e}"})

        return Response(status=status, data=data)
