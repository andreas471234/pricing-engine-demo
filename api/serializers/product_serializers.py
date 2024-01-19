from pricingapp.models import Product, ProductUnit
from rest_framework import serializers


class ProductDataSerializer(serializers.ModelSerializer):
    product_unit_name = serializers.CharField(source='unit.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'market_price', 'weight', 'created_at', 'product_unit_name')
        read_only_fields = ('id', 'created_at')


class ProductUnitDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ('id', 'name')
        read_only_fields = ('id',)
