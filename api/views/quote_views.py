import logging

from django.shortcuts import get_object_or_404
from pricingapp.models.customer import Customer
from pricingapp.models.quote import Quote
from services.utils import request_query_params_to_dict, request_pagination
from pricingapp.manager.quote_manager import QuoteManager
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


logger = logging.getLogger(__name__)


class QuoteViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="list")
    def quote_list(self, request):
        page, page_size = request_pagination(request.query_params)
        query_params = request_query_params_to_dict(request.query_params)
        resp_data = QuoteManager().get_quote_list(query_params, page, page_size)

        return Response(status=HTTP_200_OK, data=resp_data)

    @action(methods=["get"], detail=True, url_path="detail")
    def quote_detail(self, _, pk):
        quote_obj = get_object_or_404(Quote, id=pk)
        status, quote_data = QuoteManager(quote_obj=quote_obj).get_detail()
        
        return Response(status=status, data=quote_data)

    @action(methods=["get"], detail=True, url_path="pricedetail")
    def price_detail(self, _, pk):
        quote_obj = get_object_or_404(Quote, id=pk)
        status, quote_data = QuoteManager(quote_obj=quote_obj).get_detail()
        
        return Response(status=status, data=quote_data)

    @action(methods=["post"], detail=False, url_path="add-purchase-order")
    def add_purchase_order(self, request):
        cust_obj = get_object_or_404(Customer, code=request.data.get('customer_code'))
        status, data = QuoteManager(cust_obj).create_purchase_order(request.data)
        return Response(status=status, data=data)

    @action(methods=["post"], detail=False, url_path="add-product-unit")
    def add_quote_unit(self, request):
        status, data = QuoteManager().create_unit(request.data)
        return Response(status=status, data=data)
