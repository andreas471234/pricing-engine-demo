from django.db import models
from pricingapp.models.product import Product, ProductUnit

from simple_history.models import HistoricalRecords
from .common import SoftDeletionManager, SoftDeletionModel

class Supplier(SoftDeletionModel):
    code = models.CharField(
        max_length=127, null=False, unique=True, db_index=True, help_text="Supplier unique code"
    )
    name = models.CharField(max_length=127, null=False, help_text="Name of the supplier")
    address = models.TextField(null=False, help_text='Address of Supplier')
    city = models.CharField(max_length=127, null=False, help_text="City of Supplier address")
    state = models.CharField(max_length=127, null=False, help_text="State of Supplier address")
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

        supp_list = Supplier.objects.filter(**_filters).order_by("created_at").distinct()

        return supp_list


class SupplierProduct(SoftDeletionModel):
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, help_text="Foreign key of Supplier", related_name="product_maps"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, help_text="Foreign key of Product", related_name="supplier_maps"
    )
    stock = models.FloatField(default=0, help_text="Stock of product sell by supplier")
    unit = models.ForeignKey(
        ProductUnit, on_delete=models.CASCADE, help_text="Foreign key of unit for the default stock"
    )
    objects = SoftDeletionManager()


class ProductPrice(SoftDeletionModel):
    supplier_map = models.ForeignKey(
        SupplierProduct, on_delete=models.CASCADE, help_text="Foreign key of supplier product map", 
        related_name="price_maps"
    )
    price_per_unit = models.DecimalField(
        default=0.0, max_digits=25, decimal_places=4, help_text="Price per unit of product"
    )
    min_qty = models.FloatField(default=0, help_text="Minimal qty that they sell this unit in to get these prices")
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, help_text="Foreign key of unit")
    objects = SoftDeletionManager()
