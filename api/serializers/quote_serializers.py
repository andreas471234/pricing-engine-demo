from rest_framework import serializers

from pricingapp.models import Quote
from pricingapp.models.product import Product
from pricingapp.models.quote import QuoteItem
from pricingapp.settings import DATE_FORMAT


class QuoteListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    customer_code = serializers.CharField(source="customer.code", read_only=True)
    price_breakdown = serializers.JSONField(required=True)

    class Meta:
        model = Quote
        fields = (
            "id",
            "quote_no",
            "status",
            "expiry_date",
            "payable_amount",
            "price_breakdown",
            "remarks",
            "created_at",
            "customer_name",
            "customer_code",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class QuoteItemSerializer(serializers.Serializer):
    product_code = serializers.CharField(max_length=127, required=True)
    qty = serializers.FloatField(required=True, min_value=0)
    selling_price = serializers.DecimalField(
        min_value=1000, max_digits=25, decimal_places=4, required=True
    )

    class Meta:
        fields = ("product_code", "qty", "selling_price")

    def validate_product_code(self, val):
        products = Product.objects.filter(code=val)
        if not products.exists():
            raise serializers.ValidationError(f"No Product with this code - {val}")

        return val


class QuoteItemDetailSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(source="product.code")
    supplier_code = serializers.SerializerMethodField()

    class Meta:
        model = QuoteItem
        fields = (
            "product_code",
            "supplier_code",
            "order_quantity",
            "status",
            "selling_price",
            "shipping_price",
        )

    def get_supplier_code(self, obj):
        supplier = obj.supplier
        if supplier:
            return supplier.code
        return None


class OrderDetailSerializer(serializers.Serializer):
    product_code = serializers.CharField()
    supplier_code = serializers.CharField()
    supplier_city = serializers.CharField()
    qty = serializers.FloatField()
    weight = serializers.FloatField()
    price = serializers.DecimalField(max_digits=100, decimal_places=4)

    class Meta:
        fields = (
            "product_code",
            "supplier_code",
            "supplier_city",
            "qty",
            "weight",
            "price",
        )


class QuoteShippingSerializer(serializers.Serializer):
    supplier_code = serializers.CharField()
    product_list = serializers.ListField()
    total_weight = serializers.FloatField()
    shipping_price = serializers.DecimalField(max_digits=100, decimal_places=4)

    class Meta:
        fields = ("supplier_code", "product_list", "total_weight", "shipping_price")


class QuotePriceSerializer(serializers.Serializer):
    subtotal_price = serializers.DecimalField(max_digits=100, decimal_places=4)
    shipping_price = serializers.DecimalField(max_digits=100, decimal_places=4)
    total_payable = serializers.DecimalField(max_digits=100, decimal_places=4)
    orders = OrderDetailSerializer(many=True)
    shipping_details = QuoteShippingSerializer(many=True)

    class Meta:
        fields = (
            "subtotal_price",
            "shipping_price",
            "total_payable",
            "orders",
            "shipping_details",
        )


class QuoteDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    customer_code = serializers.CharField(source="customer.code", read_only=True)
    price_breakdown = serializers.JSONField(required=True)
    items = QuoteItemDetailSerializer(many=True)

    class Meta:
        model = Quote
        fields = (
            "id",
            "quote_no",
            "status",
            "expiry_date",
            "payable_amount",
            "price_breakdown",
            "remarks",
            "created_at",
            "customer_name",
            "customer_code",
            "items",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class CreatePOSerializer(serializers.Serializer):
    order_date = serializers.DateField(
        input_formats=[DATE_FORMAT, "iso-8601"], required=False
    )
    orders = serializers.ListField(
        child=QuoteItemSerializer(), min_length=1, max_length=20
    )

    class Meta:
        fields = ("order_date", "orders")

    def validate(self, attrs):
        order_item = []
        for item in attrs["orders"]:
            if item["product_code"] not in order_item:
                order_item.append(item["product_code"])
            else:
                raise serializers.ValidationError(
                    "Duplicate product code found in the order"
                )

        return attrs
