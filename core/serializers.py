from rest_framework import serializers
from .models import Device,Authenticate


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('location_ID','seed','created')

        