from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm
from .models import ServiceRequest, UserProfile, ServiceProvider, Offer


class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = '__all__'
        exclude = ['user']
        
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('__all__')
        widgets = {"is_service_provider": forms.HiddenInput(), "is_client": forms.HiddenInput(), "user": forms.HiddenInput()}

class ServiceRequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ('__all__')
        widgets = {"status": forms.HiddenInput(), "client": forms.HiddenInput()}
        

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['cost_estimate', 'completion_time']