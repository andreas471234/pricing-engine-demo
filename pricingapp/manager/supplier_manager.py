from django.core.paginator import Paginator
from django.db import transaction
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.serializers.supplier_serializers import (
    AddProductSerializer,
    ProductPriceSerializer,
    SupplierDataSerializer,
    SupplierDetailSerializer,
    SupplierProductSerializer,
)
from pricingapp.models import Supplier
from pricingapp.models.product import ProductUnit
from pricingapp.models.supplier import SupplierProduct
from services.base_manager import BaseManager


class SupplierManager(BaseManager):
    def __init__(self, obj=None):
        super().__init__()
        self.supplier_obj = obj
        self.errors = None
        self.error_code = None

    def create(self, payload):
        serializer = SupplierDataSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return HTTP_201_CREATED, serializer.data
        return HTTP_400_BAD_REQUEST, serializer.errors

    def get_detail(self):
        serializer = SupplierDetailSerializer(self.supplier_obj)

        return HTTP_200_OK, serializer.data

    @transaction.atomic
    def add_products(self, prod_obj, payload):
        serializer = AddProductSerializer(data=payload)
        if not serializer.is_valid():
            return HTTP_400_BAD_REQUEST, serializer.errors

        data = serializer.data

        supp_prod_obj, created = SupplierProduct.objects.get_or_create(
            supplier=self.supplier_obj,
            product=prod_obj,
            defaults={
                "stock": data["stock"],
                "unit": ProductUnit.objects.get(name=data.get("unit", "Batang")),
            },
        )

        if not created:
            supp_prod_obj.stock = data["stock"]
            supp_prod_obj.save()

        if not supp_prod_obj.price_maps.exists():
            data["supplier_map"] = supp_prod_obj.id
            data["unit"] = supp_prod_obj.unit.id
            serializer = ProductPriceSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        else:
            prod_prices = supp_prod_obj.price_maps.first()
            prod_prices.price_per_unit = data["price_per_unit"]
            prod_prices.save()

        serializer = SupplierProductSerializer(supp_prod_obj)

        return HTTP_201_CREATED, serializer.data

    @staticmethod
    def _get_supplier_queryset(query_params):
        filters = {
            "code": query_params.get("code", ""),
            "name": query_params.get("name", ""),
            "address": query_params.get("address", ""),
            "city": query_params.get("city", ""),
            "state": query_params.get("state", ""),
        }

        verification_queryset = Supplier.get_list(filters)

        return verification_queryset

    @classmethod
    def get_supplier_list(cls, query_params, page=None, page_size=10):
        supplier_queryset = cls._get_supplier_queryset(query_params)

        if page and page_size:
            paginator = Paginator(supplier_queryset, page_size)
            total_count = paginator.count
            num_pages = paginator.num_pages
            supplier_queryset = paginator.get_page(page)
        else:
            total_count = len(supplier_queryset)
            num_pages = 1
            page = 1

        data = SupplierDataSerializer(supplier_queryset, many=True).data
        resp = {
            "data": data,
            "meta_data": {
                "total_records": total_count,
                "page_size": page_size,
                "num_page": num_pages,
                "page": min(page, num_pages),
            },
        }

        return resp
