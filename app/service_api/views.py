from rest_framework.generics import ListAPIView, CreateAPIView
from service.models import ServiceArea, ServiceType, ServiceRequest
from .serializers import ServiceAreaSerializer, ServiceTypeSerializer, ServiceRequestSerializer

class ServiceAreaView(ListAPIView):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

class ServiceTypeView(ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

class ServiceRequestView(CreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
