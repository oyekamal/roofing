from rest_framework import serializers
from service.models import ServiceArea, ServiceType, ServiceRequest

class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ('id', 'name', 'description')

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name', 'description')

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ('full_name', 'address', 'phone_number', 'service_area', 'service_type', 'description')
