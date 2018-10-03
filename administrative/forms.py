from django import forms
from .models import *


#class ContactForm(forms.ModelForm):
#    class Meta:
#        model = Contact
#        fields = ['first_name', 'last_name', 'phone_number', 'institution']

class ProductionReportForm(forms.ModelForm):
    class Meta:
        model = ProductionReport
        fields = ['self_seed']
