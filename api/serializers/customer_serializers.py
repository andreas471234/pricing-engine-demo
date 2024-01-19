from api.serializers.quote_serializers import QuoteListSerializer
from pricingapp.models import Customer
from pricingapp.models.product import Product
from rest_framework import serializers


class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'code', 'name', 'address', 'city', 'state', 'created_at')
        read_only_fields = ('id', 'created_at')


class CustomerDetailSerializer(serializers.ModelSerializer):
    quotes = QuoteListSerializer(many=True)
    
    class Meta:
        model = Customer
        fields = ('id', 'code', 'name', 'address', 'city', 'state', 'created_at', 'quotes')
        read_only_fields = ('id', 'created_at')


class CreateQuoteItemSerializer(serializers.Serializer):
    product_code = serializers.CharField(max_length=127, required=True)
    qty = serializers.FloatField(required=True, min_value=0)

    class Meta:
        fields = ('product_code', 'qty')

    def validate_product_code(self, val):
        products = Product.objects.filter(code = val)
        if not products.exists():
            raise serializers.ValidationError(f"No Product with this code - {val}")

        return val


class CreateQuoteSerializer(serializers.Serializer):
    orders = serializers.ListField(child=CreateQuoteItemSerializer(), min_length=1, max_length=20)

    class Meta:
        fields = ('orders')

    def validate(self, attrs):
        order_item = []
        for item in attrs['orders']:
            if item['product_code'] not in order_item:
                order_item.append(item['product_code'])
            else:
                raise serializers.ValidationError(f"Duplicate product code found in the order - {item['product_code']}")

        return attrs
