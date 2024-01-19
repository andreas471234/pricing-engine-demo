from api.serializers.customer_serializers import CreateQuoteSerializer, CustomerDataSerializer, CustomerDetailSerializer
from pricingapp.manager.quote_manager import QuoteManager
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST)
from pricingapp.models import Customer
from services.base_manager import BaseManager
from django.core.paginator import Paginator


class CustomerManager(BaseManager):
    def __init__(self, cust_obj = None):
        self.cust_obj = cust_obj
        self.errors = None
        self.error_code = None

    def create(self, payload):
        serializer = CustomerDataSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return HTTP_201_CREATED, serializer.data
        return HTTP_400_BAD_REQUEST, serializer.errors

    def get_detail(self):
        serializer = CustomerDetailSerializer(self.cust_obj)
        
        return HTTP_200_OK, serializer.data
    
    def get_quote_price(self, payload):
        serializer = CreateQuoteSerializer(data=payload)
        if serializer.is_valid():
            data = serializer.data
            quote_manager = QuoteManager(cust_obj=self.cust_obj)
            status_code, resp = quote_manager.get_price(data)

            return status_code, resp
        
        return HTTP_400_BAD_REQUEST, serializer.errors
    
    def create_quote(self, payload):
        serializer = CreateQuoteSerializer(data=payload)
        if serializer.is_valid():
            data = serializer.data
            quote_manager = QuoteManager(cust_obj=self.cust_obj)
            status_code, resp = quote_manager.get_price(data)
            status_code, resp = quote_manager.create_quote(data)

            return status_code, resp
        
        return HTTP_400_BAD_REQUEST, serializer.errors
        
            
    @staticmethod
    def _get_customer_queryset(query_params):
        filters = {
            "code": query_params.get("code", ""),
            "name": query_params.get("name", ""),
            "address": query_params.get("address", ""),
            "city": query_params.get("city", ""),
            "state": query_params.get("state", ""),
        }

        verification_queryset = Customer.get_list(filters)

        return verification_queryset

    @classmethod
    def get_customer_list(cls, query_params={}, page=None, page_size=10):
        customer_queryset = cls._get_customer_queryset(query_params)

        if page and page_size:
            paginator = Paginator(customer_queryset, page_size)
            total_count = paginator.count
            num_pages = paginator.num_pages
            customer_queryset = paginator.get_page(page)
        else:
            total_count = len(customer_queryset)
            num_pages = 1
            page = 1
    
        data = CustomerDataSerializer(customer_queryset, many=True).data
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
