from .models import ServiceProvider

def service_providers(request):
    all_service_providers = ServiceProvider.objects.all()
    user_service_provider = None
    if request.user.is_authenticated:
        user_service_provider = ServiceProvider.objects.filter(user=request.user).first()
    return {
        'all_service_providers': all_service_providers,
        'user_service_provider': user_service_provider
    }