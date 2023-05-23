from django.urls import path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.home, name="home"),
    path("service_request/", views.service_request, name="service_request"),
    path("service_request_list/", views.service_request_list, name="service_request_list"),
    # path('<int:pk>/update/', views.service_request_update, name='service_request_update'),
    # path('<int:pk>/delete/', views.service_request_delete, name='service_request_delete'),
]