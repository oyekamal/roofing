from django.urls import path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.home, name="home"),
    path("service_request/", views.service_request, name="service_request_form"),
    path("service_request_list/", views.service_request_list,
         name="service_request_list"),
    path('service_request_delete/<int:pk>/',
         views.ServiceRequestDeleteView.as_view(), name='service_request_delete'),
    path('service_request_update/<int:pk>/',
         views.ServiceRequestUpdateView.as_view(), name='service_request_update'),

    path('service_request/<int:pk>/', views.ServiceRequestDetailView.as_view(),
         name='service_request_detail'),
    path('offer/<int:pk>/', views.OfferDetailView.as_view(), name='offer_detail'),

    # service_provider
    path('service_providers/', views.ServiceProviderListView.as_view(),
         name='service_provider_list'),
    path('service_providers/create/', views.ServiceProviderCreateView.as_view(),
         name='service_provider_create'),
    path('service_providers/<int:pk>/update/',
         views.ServiceProviderUpdateView.as_view(), name='service_provider_update'),
    path('service_providers/<int:pk>/delete/',
         views.ServiceProviderDeleteView.as_view(), name='service_provider_delete'),
    path('service_providers/<int:pk>/',
         views.ServiceProviderDetailView.as_view(), name='service_provider_detail'),
    path('client_service_request_list/', views.client_service_request_list, name='client_service_request_list'),
    path('client_service_request_offer/<int:service_request_id>', views.client_service_request_offer, name='client_service_request_offer'),
    
    path('service_providers/<int:service_provider_id>/previous_work_list/', views.previous_work_list, name='previous_work_list'),
    path('service_providers/<int:service_provider_id>/previous_work_create/', views.previous_work_create, name='previous_work_create'),
    path('service_providers/<int:service_provider_id>/previous_work_update/<int:previous_work_id>/', views.previous_work_update, name='previous_work_update'),
    path('service_providers/<int:service_provider_id>/previous_work_delete/<int:previous_work_id>/', views.previous_work_delete, name='previous_work_delete'),
     
]
