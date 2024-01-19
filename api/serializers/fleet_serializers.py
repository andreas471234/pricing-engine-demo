from pricingapp.models import Fleet
from rest_framework import serializers


class FleetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ('id', 'code', 'name', 'capacity', 'pool', 'cost', 'type', 'created_at')
        read_only_fields = ('id', 'created_at')
