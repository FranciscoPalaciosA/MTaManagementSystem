from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from .forms import *

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Administrative Index")

@login_required
def production_report(request):
    return render(request, 'administrative/Production_Report.html')

def add_production_report(request):
    if request.method == 'POST':
        form = ProductionReportForm(request.POST)

        if form.is_valid():
            if not form.cleaned_data['exch_seed']:
                exch_seed = 0
            else:
                exch_seed = form.cleaned_data['exch_seed']

            if not form.cleaned_data['exch_leaf']:
                exch_leaf = 0
            else:
                exch_leaf = form.cleaned_data['exch_leaf']
            if not form.cleaned_data['want_for_seed']:
                want_for_seed = ' '
            else:
                want_for_seed = form.cleaned_data['want_for_seed']
            if not form.cleaned_data['want_for_leaf']:
                want_for_leaf = ' '
            else:
                want_for_leaf = form.cleaned_data['want_for_leaf']

            newProductionReport = ProductionReport(
                                                    beneficiary = Beneficiary.objects.get(id = 1),
                                                    self_seed = form.cleaned_data['self_seed'],
                                                    self_leaf = form.cleaned_data['self_leaf'],
                                                    self_flour = form.cleaned_data['self_seed'],
                                                    days_per_month = form.cleaned_data['days_per_month'],
                                                    exch_seed = exch_seed,
                                                    want_for_seed = want_for_seed,
                                                    exch_leaf = exch_leaf,
                                                    want_for_leaf = want_for_leaf
                                                    )
            newProductionReport.save()
            return HttpResponseRedirect('/administrative/')

        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")

@login_required
def beneficiaries(request):
    form = BeneficiaryForm()
    beneficiary_in_program_form = BeneficiaryInProgram()
    context = {'form': form, 'beneficiary_in_program_form': beneficiary_in_program_form}
    return render(request, 'administrative/beneficiaries.html', context)

@login_required
def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if all([form.is_valid()]):
            print("Promoter =" + str(form.cleaned_data['promoter']))
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

            print("Ben:"+ str(beneficiary))
            beneficiary.save()

            benficiary_in_program = BeneficiaryInProgram(
                                                        beneficiary=beneficiary,
                                                        program=Program(id=form.cleaned_data['member_in']),
                                                        curp=form.cleaned_data['curp'],
                                                        house_address=form.cleaned_data['house_address'],
                                                        house_references=form.cleaned_data['house_references'],
                                                        huerto_coordinates=form.cleaned_data['huerto_coordinates'],
                                                        water_capacity=form.cleaned_data['water_capacity'],
                                                        savings_account_role=form.cleaned_data['savings_account_role']
                                                        )
            beneficiary_in_program.save()
            return HttpResponseRedirect('/administrative/beneficiaries')
        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")
            #print(program_form.errors)
            print("\n\n\n\n\n")

    elif request.method == 'GET':
        form = BeneficiaryForm()
        context = {'form': form}
        return render(request, 'administrative/new_beneficiary.html', context)


@login_required
def weekly_sessions(request):
    if request.method == 'POST':
        form = WeeklySessionForm(request.POST)
        if form.is_valid():
            base_user = BaseUser.objects.get(user = request.user.id)
            promoter = Promoter.objects.get(base_user = base_user.id)
            newSession = WeeklySession(
                                        promoter=promoter,
                                        type=form.cleaned_data['type'],
                                        topic=form.cleaned_data['topic'],
                                        start_time=form.cleaned_data['start_time'],
                                        end_time=form.cleaned_data['end_time'],
                                       )
            newSession.save()

            list = request.POST.getlist("assistants")
            for assistant in list:
                newSession.assistants.add(Beneficiary.objects.get(id = assistant))

            return HttpResponseRedirect('/administrative/weekly_sessions/')
        else:
            print("-------------------")
            print("Form is not valid")
            print(form.errors)
    else:
        weekly_session_form = WeeklySessionForm()
        context = {'weekly_session_form': weekly_session_form}
        return render(request, 'administrative/weekly_sessions.html', context)
