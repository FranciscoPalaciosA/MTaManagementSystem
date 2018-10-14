from django import forms
from .models import *
from administrative.models import Community
from django.contrib.auth.models import Group

class AlertForm(forms.ModelForm):
    class Meta:
        model = HelpAlert
        fields = ['name', 'description']

class PromoterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    name = forms.CharField(max_length=50)
    last_name_paternal = forms.CharField(max_length=50)
    last_name_maternal = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    communities = forms.ModelMultipleChoiceField(queryset = Community.objects.all())
    contact_name = forms.CharField(max_length=50)
    contact_phone_number = forms.CharField(max_length=50)

class BaseUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    group = forms.ModelChoiceField(queryset = Group.objects.all())
    name = forms.CharField(max_length=50)
    last_name_paternal = forms.CharField(max_length=50)
    last_name_maternal = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
