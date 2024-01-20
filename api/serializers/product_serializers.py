from rest_framework import serializers

from pricingapp.models import Product, ProductUnit


class ProductDataSerializer(serializers.ModelSerializer):
    product_unit_name = serializers.CharField(source="unit.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "code",
            "name",
            "weight",
            "created_at",
            "product_unit_name",
            "unit"
        )
        read_only_fields = ("id", "created_at")
        extra_kwargs = {
            "unit": {"write_only": True},
        }


class ProductUnitDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ("id", "name")
        read_only_fields = ("id",)
