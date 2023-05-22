# from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm
from .models import ServiceRequest

class ServiceRequestForm(ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["mouth"].queryset = Mouth.objects.filter(
    #         Q(user=user) | Q(user__username="admin")
    #     )

    class Meta:
        model = ServiceRequest
        fields = ('__all__')
        # fields = ("audio", "script", "name", "host", "mouth", "user")
        # widgets = {"host": forms.HiddenInput(), "user": forms.HiddenInput()}