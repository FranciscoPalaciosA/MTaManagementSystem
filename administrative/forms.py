from django import forms
from.models import *
from profiles.models import *

class BeneficiaryForm(forms.Form):
    name = forms.CharField(max_length=50)
    last_name_paternal = forms.CharField(max_length=50)
    last_name_maternal = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    municipality = forms.CharField(max_length=50)
    community_name = forms.CharField(max_length=50)
    num_of_family_beneficiaries = forms.IntegerField(required=True)
    contact_name = forms.CharField(max_length=200)
    contact_phone = forms.IntegerField()
    account_number = forms.IntegerField()
    bank_name = forms.CharField(max_length=100)
    promoter = forms.ModelMultipleChoiceField(queryset=Promoter.objects)
    member_in = forms.ModelMultipleChoiceField(queryset=Program.objects)
    curp = forms.CharField(max_length=50, required=False)
    house_address = forms.CharField(max_length=100, required=False)
    house_references = forms.CharField(max_length=120, required=False)
    huerto_coordinates = forms.CharField(max_length=100, required=False)
    water_capacity = forms.IntegerField(required=False)
    cisterna_location = forms.CharField(max_length=120, required=False)
    cisterna_status = forms.CharField(max_length=120, required=False)
    school = forms.CharField(max_length=120, required=False)
    age = forms.IntegerField(required=False)
    initial_weight = forms.DecimalField(required=False)
    savings_account_role = forms.CharField(required=False)

class BeneficiaryInProgramForm(forms.ModelForm):
    curp = forms.CharField(required=False)
    house_address = forms.CharField(required=False)
    house_references = forms.CharField(required=False)
    huerto_coordinates = forms.CharField(required=False)
    water_capacity = forms.IntegerField(required=False)
    cisterna_location = forms.CharField(required=False)
    cisterna_status = forms.CharField(required=False)
    school = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    initial_weight = forms.DecimalField(required=False)
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
                    'cisterna_location',
                    'cisterna_status',
                    'school',
                    'age',
                    'initial_weight',
                    'savings_account_role'
                ]

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name',
                  'municipality',
                  'state']

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
