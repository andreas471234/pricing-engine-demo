from django.db import models
from pricingapp.models.product import ProductUnit

from simple_history.models import HistoricalRecords
from .common import SoftDeletionManager, SoftDeletionModel
from django.db.models import Q

class Fleet(SoftDeletionModel):
    FLEET_GROUND = "GROUND"
    FLEET_TYPE = (
        (FLEET_GROUND, FLEET_GROUND,),
    )

    code = models.CharField(
        max_length=127, null=False, unique=True, db_index=True, help_text="Fleet unique code"
    )
    name = models.CharField(max_length=127, null=False, help_text="Fleet name")
    capacity = models.FloatField(null=False, help_text="Fleet max capacity")
    cost = models.JSONField(null=False, help_text="Fleet cost", default=dict)
    type = models.CharField(max_length=127, choices=FLEET_TYPE, default=FLEET_GROUND, help_text="Fleet type")
    pool = models.CharField(max_length=127, null=False, help_text="Fleet pool to calculate the shipping cost")
    objects = SoftDeletionManager()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.code} - {self.name}"

    @classmethod
    def calculate_price(cls, weight, supp_city, cust_city):
        obj_list = cls.objects.filter(capacity__gte=weight)
        cust_shipping_prices = []
        for obj in obj_list:
            if obj.cost.get(cust_city):
                cust_shipping_prices.append(obj.cost.get(cust_city))
        if len(cust_shipping_prices) == 0:
            return 0, "city not found for shipping"
        cust_shipping = min(cust_shipping_prices)

        supp_shipping_prices = []
        for obj in obj_list:
            if obj.cost.get(supp_city):
                supp_shipping_prices.append(obj.cost.get(supp_city))
        if len(supp_shipping_prices) == 0:
            return 0, "city not found for shipping"
        supp_shipping = min(supp_shipping_prices)

        return max([cust_shipping, supp_shipping]), None

    @staticmethod
    def get_list(filters):
        field_filter_map = {
            "code": "Q(code__icontains='{data}')",
            "name": "Q(name__icontains='{data}')",
            "pool": "Q(pool__icontains='{data}')",
            "type": "Q(type__in={data})",
        }


        _filter_query = ""
        for filter_key, field_name in field_filter_map.items():
            data = filters.get(filter_key)
            if data not in (None, list(), dict(), "", ['']):
                if _filter_query == "":
                    _filter_query += field_name.format(data=data)
                else:
                    _filter_query += "&" + field_name.format(data=data)

        fleet_list = Fleet.objects.all()
        if _filter_query != '':
            fleet_list = fleet_list.filter(eval(_filter_query))

        fleet_list = fleet_list.order_by("created_at").distinct()

        return fleet_list
