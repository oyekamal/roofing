from django.urls import path
from .views import ServiceAreaView, ServiceTypeView, ServiceRequestView

urlpatterns = [
    path('service-area/', ServiceAreaView.as_view(), name='service_area'),
    path('service-type/', ServiceTypeView.as_view(), name='service_type'),
    path('service-request/', ServiceRequestView.as_view(), name='service_request'),
]
