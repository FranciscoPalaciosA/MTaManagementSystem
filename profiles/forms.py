from django import forms
from .models import *

class AlertForm(forms.ModelForm):
    class Meta:
        model = HelpAlert
        fields = ['name', 'description']
