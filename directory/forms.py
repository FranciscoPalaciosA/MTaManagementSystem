from django import forms
from .models import *

#Form used to register Contacts in new_contact
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name',
                  'last_name_paternal',
                  'last_name_maternal',
                  'phone_number',
                  'email',
                  'contact_type',
                  'institution',
                  'comments']
#Form used to register Institutions in new_institution
class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name',
                  'type_of_institution',
                  'comments']
