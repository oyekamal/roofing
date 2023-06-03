from django.contrib import admin

from .models import UserProfile, ServiceArea, ServiceType, ServiceRequest, ServiceProvider, PreviousWork, Offer, ChatMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'address',
        'phone_number',
        'is_service_provider',
        'is_client',
    )
    list_filter = ('user', 'is_service_provider', 'is_client')


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'service_area',
        'service_type',
        'description',
        'created_at',
        'status',
    )
    list_filter = ('client', 'service_area', 'service_type', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'business_name',
        'company_logo',
        'company_description',
    )
    list_filter = ('user',)


@admin.register(PreviousWork)
class PreviousWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'image', 'description')
    list_filter = ('service_provider',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service_provider',
        'service_request',
        'cost_estimate',
        'completion_time',
        'status',
    )
    list_filter = ('service_provider', 'service_request')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'service_request',
        'message',
        'timestamp',
    )
    list_filter = ('sender', 'receiver', 'service_request', 'timestamp')