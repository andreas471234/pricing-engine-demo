from django.core.paginator import Paginator
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.serializers.fleet_serializers import FleetDataSerializer
from pricingapp.models import Fleet
from services.base_manager import BaseManager


class FleetManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.errors = None
        self.error_code = None

    def create(self, payload):
        serializer = FleetDataSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return HTTP_201_CREATED, serializer.data
        return HTTP_400_BAD_REQUEST, serializer.errors

    @staticmethod
    def _get_fleet_queryset(query_params):
        filters = {
            "code": query_params.get("code", ""),
            "name": query_params.get("name", ""),
            "type": query_params.get("type", ""),
            "pool": query_params.get("pool", ""),
        }

        verification_queryset = Fleet.get_list(filters)

        return verification_queryset

    @classmethod
    def get_fleet_list(cls, query_params, page=None, page_size=10):
        fleet_queryset = cls._get_fleet_queryset(query_params)

        if page and page_size:
            paginator = Paginator(fleet_queryset, page_size)
            total_count = paginator.count
            num_pages = paginator.num_pages
            fleet_queryset = paginator.get_page(page)
        else:
            total_count = len(fleet_queryset)
            num_pages = 1
            page = 1

        data = FleetDataSerializer(fleet_queryset, many=True).data
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
