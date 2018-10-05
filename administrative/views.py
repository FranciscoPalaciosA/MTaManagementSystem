from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from.models import *
from.forms import *

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Administrative Index")

@login_required
def fill_Production_Report(request):
    return render(request, 'administrative/Production_Report.html')

@login_required
def beneficiaries(request):
    form = BeneficiaryForm()
    context = {'form': form}
    return render(request, 'administrative/beneficiaries.html', context)

@login_required
def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            beneficiary = Beneficiary   (
                                        name=form.cleaned_data['name'],
                                        last_name_paternal=form.cleaned_data['last_name_paternal'],
                                        last_name_maternal=form.cleaned_data['last_name_maternal'],
                                        state=form.cleaned_data['state'],
                                        municipality=form.cleaned_data['municipality'],
                                        community_name=form.cleaned_data['community_name'],
                                        num_of_family_beneficiaries=form.cleaned_data['num_of_family_beneficiaries'],
                                        contact_name=form.cleaned_data['contact_name'],
                                        contact_phone=form.cleaned_data['contact_phone'],
                                        account_number=form.cleaned_data['account_number'],
                                        bank_name=form.cleaned_data['bank_name'],
                                        promoter=form.cleaned_data['promoter']
                                        )

            beneficiary.save()
            return HttpResponseRedirect('/administrative/beneficiaries')
    else:
        print("-------------------")
        print("\n\n\n\n\n")
        print("Form is not valid")
        print(form.errors)
        print("\n\n\n\n\n")
