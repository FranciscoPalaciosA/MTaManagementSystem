from django import forms
from .models import *

class BeneficiaryForm(forms.ModelForm):
    class Meta:
    model = Beneficiary
    fields = ['name','last_name_paternal','last_name_maternal','state','municipality','community_name','num_of_family_beneficiaries','contact_name','contact_phone','account_number','bank_name']    
