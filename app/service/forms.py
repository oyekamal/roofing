from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm
from .models import ServiceRequest, UserProfile




class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('__all__')
        # widgets = {"status": forms.HiddenInput(), "user": forms.HiddenInput()}

class ServiceRequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ('__all__')
        widgets = {"status": forms.HiddenInput(), "client": forms.HiddenInput()}
        
    