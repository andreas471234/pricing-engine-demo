import datetime

from django.db import models
from django.db.models import Q    # trunk-ignore(ruff/F401)
from sequences import get_next_value
from simple_history.models import HistoricalRecords

from pricingapp.models.customer import Customer
from pricingapp.models.product import Product
from pricingapp.models.supplier import Supplier

from .common import SoftDeletionManager, SoftDeletionModel


def generate_application_no():
    creation_date = datetime.datetime.now()
    prefix = creation_date.strftime("%y%m")
    nxt_val = get_next_value(f"application{prefix}")
    return f"RFQ-{prefix}{nxt_val:06}"


class Quote(SoftDeletionModel):
    STATUS_INITIATED = "INITIATED"
    STATUS_PENDING = "PENDING"
    STATUS_INPROGRESS = "INPROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_EXPIRED = "EXPIRED"
    STATUS_CHOICES = (
        (
            STATUS_INITIATED,
            STATUS_INITIATED,
        ),
        (
            STATUS_PENDING,
            STATUS_PENDING,
        ),
        (
            STATUS_INPROGRESS,
            STATUS_INPROGRESS,
        ),
        (
            STATUS_COMPLETED,
            STATUS_COMPLETED,
        ),
        (
            STATUS_CANCELLED,
            STATUS_CANCELLED,
        ),
        (
            STATUS_EXPIRED,
            STATUS_EXPIRED,
        ),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        help_text="Foreign key of Customer",
        related_name="quotes",
    )
    quote_no = models.CharField(
        max_length=15, unique=True, null=False, default=generate_application_no
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_INITIATED, db_index=True
    )
    expiry_date = models.DateTimeField(
        blank=True, null=True, help_text="Date of the expiry of quote if given"
    )
    payable_amount = models.DecimalField(
        default=0.0,
        max_digits=30,
        decimal_places=4,
        help_text="Total Payable that customer need to pay",
    )
    price_breakdown = models.JSONField(
        null=False, default=dict, help_text="Breakdown of the total price"
    )
    remarks = models.TextField(null=True, blank=True, help_text="Remarks of the quote")
    objects = SoftDeletionManager()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.quote_no)

    @staticmethod
    def get_list(filters):
        field_filter_map = {
            "quote_no": "Q(quote_no__icontains='{data}')",
            "name": "Q(customer__name__icontains='{data}')",
            "code": "Q(customer__code__icontains='{data}')",
            "status": "Q(status__in={data})",
        }

        _filter_query = ""
        for filter_key, field_name in field_filter_map.items():
            data = filters.get(filter_key)
            if data not in (None, list(), dict(), "", [""]):
                if _filter_query == "":
                    _filter_query += field_name.format(data=data)
                else:
                    _filter_query += "&" + field_name.format(data=data)

        quote_list = Quote.objects.all()
        if _filter_query != "":
            quote_list = quote_list.filter(eval(_filter_query))

        quote_list = quote_list.order_by("created_at").distinct()

        return quote_list


class QuoteItem(SoftDeletionModel):
    STATUS_INITIATED = "INITIATED"
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = (
        (
            STATUS_INITIATED,
            STATUS_INITIATED,
        ),
        (
            STATUS_PENDING,
            STATUS_PENDING,
        ),
        (
            STATUS_APPROVED,
            STATUS_APPROVED,
        ),
        (
            STATUS_COMPLETED,
            STATUS_COMPLETED,
        ),
        (
            STATUS_CANCELLED,
            STATUS_CANCELLED,
        ),
    )

    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        help_text="Foreign key of Quote",
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Foreign key of Product",
        related_name="quote_items",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        null=True,
        help_text="Foreign key of Supplier",
        related_name="quote_items",
    )
    remarks = models.TextField(
        null=True, blank=True, help_text="Remarks of the quote item"
    )
    order_quantity = models.FloatField(
        default=1, help_text="Quantity of ordered product"
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_INITIATED, db_index=True
    )
    selling_price = models.DecimalField(
        default=0.0, max_digits=25, decimal_places=4, help_text="Selling price per unit"
    )
    shipping_price = models.DecimalField(
        default=0.0,
        max_digits=25,
        decimal_places=4,
        help_text="Shipping price of the item",
    )
    objects = SoftDeletionManager()
    history = HistoricalRecords()
