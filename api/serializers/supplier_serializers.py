from rest_framework import serializers

from pricingapp.models import Supplier
from pricingapp.models.supplier import ProductPrice, SupplierProduct


class SupplierDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "code", "name", "address", "city", "state", "created_at")
        read_only_fields = ("id", "created_at")


class AddProductSerializer(serializers.Serializer):
    product_code = serializers.CharField(max_length=127, allow_blank=False)
    price_per_unit = serializers.DecimalField(
        min_value=1000, max_digits=25, decimal_places=4
    )
    stock = serializers.FloatField(default=0, required=False)
    unit = serializers.CharField(max_length=127, required=False, allow_blank=True)

    class Meta:
        fields = ("product_code", "price_per_unit", "stock", "unit")


class ProductPriceSerializer(serializers.ModelSerializer):
    price_per_unit = serializers.DecimalField(
        min_value=1000, max_digits=25, decimal_places=4
    )

    class Meta:
        model = ProductPrice
        fields = (
            "id",
            "price_per_unit",
            "min_qty",
            "updated_at",
            "created_at",
            "supplier_map",
            "unit",
        )
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "supplier_map": {"write_only": True},
            "unit": {"write_only": True},
        }


class SupplierProductSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(source="price_maps", many=True)
    product_code = serializers.CharField(source="product.code", read_only=True)
    product_unit_name = serializers.CharField(source="unit.name", read_only=True)

    class Meta:
        model = SupplierProduct
        fields = (
            "id",
            "product_code",
            "stock",
            "product_unit_name",
            "created_at",
            "prices",
        )
        read_only_fields = ("id", "created_at")


class SupplierDetailSerializer(serializers.ModelSerializer):
    products = SupplierProductSerializer(source="product_maps", many=True)

    class Meta:
        model = Supplier
        fields = (
            "id",
            "code",
            "name",
            "address",
            "city",
            "state",
            "created_at",
            "products",
        )
        read_only_fields = ("id", "created_at")
