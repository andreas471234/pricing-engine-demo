import logging
from services.utils import request_pagination, request_query_params_to_dict
from pricingapp.manager.fleet_manager import FleetManager
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


logger = logging.getLogger(__name__)


class FleetViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="list")
    def fleet_list(self, request):
        page, page_size = request_pagination(request.query_params)
        query_params = request_query_params_to_dict(request.query_params)
        resp_data = FleetManager().get_fleet_list(query_params, page, page_size)

        return Response(status=HTTP_200_OK, data=resp_data)

    @action(methods=["post"], detail=False, url_path="add-fleet")
    def add_fleet(self, request):
        status, data = FleetManager().create(request.data)
        return Response(status=status, data=data)
