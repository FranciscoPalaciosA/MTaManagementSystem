from django import forms
from.models import *

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = [      'name',
                        'last_name_paternal',
                        'last_name_maternal',
                        'state','municipality',
                        'community_name',
                        'num_of_family_beneficiaries',
                        'contact_name',
                        'contact_phone',
                        'account_number',
                        'bank_name',
                        'promoter']

class ProductionReportForm(forms.ModelForm):
    exch_seed = forms.DecimalField(required=False)
    exch_leaf = forms.DecimalField(required=False)

    class Meta:
        model = ProductionReport
        fields = [  'self_seed',
                    'self_leaf',
                    'self_flour',
                    'days_per_month',
                    'exch_seed',
                    'exch_leaf']
   
class WeeklySessionForm(forms.ModelForm):
    class Meta:
        model = WeeklySession
        fields = ['type', 'topic', 'assistants', 'start_time', 'end_time']

        widgets = {
            'assistants': forms.CheckboxSelectMultiple,
        }
