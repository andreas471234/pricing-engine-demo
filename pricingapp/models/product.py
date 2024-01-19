from django.db import models

from simple_history.models import HistoricalRecords
from .common import SoftDeletionManager, SoftDeletionModel


class ProductUnit(SoftDeletionModel):
    name = models.CharField(max_length=127, null=False, help_text="Product unit name")
    objects = SoftDeletionManager()
    history = HistoricalRecords()

class Product(SoftDeletionModel):
    code = models.CharField(
        max_length=127, null=False, unique=True, db_index=True, help_text="Product unique code"
    )
    name = models.CharField(max_length=127, null=False, help_text="Product name")
    market_price = models.DecimalField(
        default=0.0, max_digits=25, decimal_places=4, help_text="Market price per unit of product"
    )
    weight = models.FloatField(default=0, help_text="Weight of the product in kg")
    unit = models.ForeignKey(
        ProductUnit, on_delete=models.CASCADE, null=True, help_text="Foreign key of Product unit",
        related_name="products"
    )
    objects = SoftDeletionManager()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.code} - {self.name}"

    @staticmethod
    def get_list(filters):
        field_filter_map = {
            "code": "code__icontains",
            "name": "name__icontains",
        }

        _filters = dict()
        for filter_key, field_name in field_filter_map.items():
            data = filters.get(filter_key)
            if data not in (None, list(), dict(), "", [""]):
                _filters[field_name] = data

        product_list = Product.objects.filter(**_filters).order_by("created_at").distinct()

        return product_list

