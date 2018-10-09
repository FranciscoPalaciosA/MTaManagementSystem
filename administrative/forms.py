from django import forms
from.models import *

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = [      'name',
                        'last_name_paternal',
                        'last_name_maternal',
                        'state',
                        'municipality',
                        'community_name',
                        'num_of_family_beneficiaries',
                        'contact_name',
                        'contact_phone',
                        'account_number',
                        'bank_name',
                        'member_in',
                        'promoter']

class BeneficiaryInProgramForm(forms.ModelForm):
    curp = forms.CharField(required=False)
    house_address = forms.CharField(required=False)
    house_references = forms.CharField(required=False)
    huerto_coordinates = forms.CharField(required=False)
    water_capacity = forms.IntegerField(required=False)
    savings_account_role = forms.CharField(required=False)

    class Meta:
        model = BeneficiaryInProgram
        fields = [
                    'program',
                    'curp',
                    'house_address',
                    'house_references',
                    'huerto_coordinates',
                    'water_capacity',
                    'savings_account_role'
                ]

class ProductionReportForm(forms.ModelForm):
    exch_seed = forms.DecimalField(required=False)
    exch_leaf = forms.DecimalField(required=False)
    want_for_seed = forms.CharField(required=False)
    want_for_leaf = forms.CharField(required=False)

    class Meta:
        model = ProductionReport
        fields = [  'self_seed',
                    'self_leaf',
                    'self_flour',
                    'days_per_month',
                    'exch_seed',
                    'want_for_seed',
                    'exch_leaf',
                    'want_for_leaf']

class WeeklySessionForm(forms.ModelForm):
    class Meta:
        model = WeeklySession
        fields = ['type', 'topic', 'assistants', 'start_time', 'end_time']

        widgets = {
            'assistants': forms.CheckboxSelectMultiple,
        }
