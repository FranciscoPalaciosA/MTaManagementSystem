from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name',
                  'last_name_paternal',
                  'last_name_maternal',
                  'phone_number',
                  'email',
                  'contact_type',
                  'comments']
                  
class ContactTypeForm(forms.ModelForm):
        model = ContactTypeInfo
        fields = ['institution']
