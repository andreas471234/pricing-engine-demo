from django.db import models

from simple_history.models import HistoricalRecords
from .common import SoftDeletionManager, SoftDeletionModel

class Customer(SoftDeletionModel):
    code = models.CharField(
        max_length=127, null=False, blank=False, unique=True, db_index=True, help_text="Customer unique code"
    )
    name = models.CharField(max_length=127, null=False, help_text="Name of the customer")
    address = models.TextField(null=False, help_text='Address of Customer')
    city = models.CharField(max_length=127, null=False, help_text="City of Customer address")
    state = models.CharField(max_length=127, null=False, help_text="State of Customer address")
    objects = SoftDeletionManager()
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.code} - {self.name}"

    @staticmethod
    def get_list(filters):
        field_filter_map = {
            "code": "code__icontains",
            "name": "name__icontains",
            "address": "address__icontains",
            "city": "city",
            "state": "state",
        }

        _filters = dict()
        for filter_key, field_name in field_filter_map.items():
            data = filters.get(filter_key)
            if data not in (None, list(), dict(), "", [""]):
                _filters[field_name] = data

        cust_list = Customer.objects.filter(**_filters).order_by("created_at").distinct()

        return cust_list
