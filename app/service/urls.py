from django.urls import path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.home, name="home"),
    path("service_request/", views.service_request, name="service_request_form"),
    path("service_request_list/", views.service_request_list, name="service_request_list"),
    path('service_request_delete/<int:pk>/', views.ServiceRequestDeleteView.as_view(), name='service_request_delete'),

]