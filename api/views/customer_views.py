import logging

from django.shortcuts import get_object_or_404
from pricingapp.models.customer import Customer
from services.utils import request_pagination, request_query_params_to_dict
from pricingapp.manager.customer_manager import CustomerManager
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


logger = logging.getLogger(__name__)


class CustomerViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="list")
    def customer_list(self, request):
        page, page_size = request_pagination(request.query_params)
        query_params = request_query_params_to_dict(request.query_params)
        resp_data = CustomerManager().get_customer_list(query_params, page, page_size)

        return Response(status=HTTP_200_OK, data=resp_data)

    @action(methods=["post"], detail=False, url_path="add-customer")
    def add_customer(self, request):
        status, data = CustomerManager().create(request.data)
        return Response(status=status, data=data)

    @action(methods=["get"], detail=True, url_path="detail")
    def customer_detail(self, _, pk):
        cust_obj = get_object_or_404(Customer, id=pk)
        status, supplier_data = CustomerManager(cust_obj).get_detail()
        
        return Response(status=status, data=supplier_data)
    
    @action(methods=["post"], detail=True, url_path="get-price")
    def get_quote_price(self, request, pk):
        cust_obj = get_object_or_404(Customer, id=pk)
        status, supplier_data = CustomerManager(cust_obj).get_quote_price(request.data)
        
        return Response(status=status, data=supplier_data)
    
    @action(methods=["post"], detail=True, url_path="create-quote")
    def create_cust_quote(self, request, pk):
        cust_obj = get_object_or_404(Customer, id=pk)
        status, supplier_data = CustomerManager(cust_obj).create_quote(request.data)
        
        return Response(status=status, data=supplier_data)
    
