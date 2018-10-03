from django import forms
from .models import *

class BeneficiaryForm(forms.ModelForm):
    class Meta:
    model = Beneficiary
    name = forms.CharField(max_length=50)
    last_name_paternal = forms.CharField(max_length=50)
    last_name_maternal = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    municipality = forms.CharField(max_length=50)
    community_name = forms.CharField(max_length=50)
    num_of_family_beneficiaries = forms.IntegerField(default=0)
    contact_name = forms.CharField(max_length=200)
    contact_phone = forms.IntegerField(default=0)
    account_number = forms.IntegerField(default=0)
    bank_name = forms.CharField(max_length=100)
