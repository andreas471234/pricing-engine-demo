from api.serializers.product_serializers import ProductDataSerializer, ProductUnitDataSerializer
from rest_framework.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST)
from pricingapp.models import Product
from services.base_manager import BaseManager
from django.core.paginator import Paginator


class ProductManager(BaseManager):
    def __init__(self):
        self.errors = None
        self.error_code = None

    def create(self, payload):
        serializer = ProductDataSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return HTTP_201_CREATED, serializer.data
        return HTTP_400_BAD_REQUEST, serializer.errors
    
    def create_unit(self, payload):
        serializer = ProductUnitDataSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return HTTP_201_CREATED, serializer.data
        return HTTP_400_BAD_REQUEST, serializer.errors
            
    @staticmethod
    def _get_product_queryset(query_params):
        filters = {
            "code": query_params.get("code", ""),
            "name": query_params.get("name", ""),
        }

        verification_queryset = Product.get_list(filters)

        return verification_queryset

    @classmethod
    def get_product_list(cls, query_params={}, page=None, page_size=10):
        product_queryset = cls._get_product_queryset(query_params)

        if page and page_size:
            paginator = Paginator(product_queryset, page_size)
            total_count = paginator.count
            num_pages = paginator.num_pages
            product_queryset = paginator.get_page(page)
        else:
            total_count = len(product_queryset)
            num_pages = 1
            page = 1
    
        data = ProductDataSerializer(product_queryset, many=True).data
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
