"""
Created by: Django
Description: Functions for handling requests to the server
Modified by: Bernardo, Hugo, Alex, Francisco
Modify date: 19/10/2018
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib import messages
from django.utils import timezone

from profiles.models import HelpAlert
from django.http import Http404
from .models import *
from .forms import *
from datetime import datetime, time

def is_promoter(user):
    #Description: Check if a user is a promoter
    #Parameter: user
    #Return: boolean indicating wheter the user is a promoter
    base = BaseUser.objects.get(pk=user.id)
    try:
        promoter = Promoter.objects.get(pk=base.id)
    except Promoter.DoesNotExist:
        return False
    return True


# Create your views here.
@login_required
def index(request):
    return HttpResponse("Administrative Index")

@login_required
def production_report(request):
    production_report_form = ProductionReportForm()
    context = {'production_report_form': production_report_form}
    return render(request, 'administrative/Production_Report.html', context)

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
    else:
        print("no entro al post")
        print(request.method)

@login_required
def production_report_list(request):
    if request.method == 'GET':
        review_reports = ProductionReport.objects.exclude(exch_seed=0).filter(get_for_seed_qty=0).exclude(paid=True) | ProductionReport.objects.exclude(exch_leaf=0).filter(get_for_leaf_qty=0).exclude(paid=True)
        pending_reports = ProductionReport.objects.exclude(paid=True).exclude(exch_seed=0).exclude(exch_seed=0).exclude(get_for_seed_qty=0).exclude(get_for_leaf_qty=0)
        paid_reports = ProductionReport.objects.filter(paid=True)
        return render(request, 'administrative/production_report_list.html', {'review_reports': review_reports, 'paid_reports': paid_reports, 'pending_reports': pending_reports})

@login_required
def beneficiaries(request, pk):
    if request.method == 'GET':
        if pk == 0:
            form = BeneficiaryForm()
            context = {'form': form}
            return render(request, 'administrative/beneficiaries.html', context)
        else:
            try:
                beneficiary = Beneficiary.objects.get(pk=pk)
            except Beneficiary.DoesNotExist:
                raise Http404("No existe ese benficiario.")

            programs = BeneficiaryInProgram.objects.filter(beneficiary=beneficiary)
            allowed_programs = Program.objects.all()
            for prog in programs:
                allowed_programs = allowed_programs.exclude(id=prog.program.id)

            form = BeneficiaryInProgramForm()
            context = {'form': form, 'beneficiary': beneficiary, 'programs': programs, 'allowed_programs': allowed_programs}
            return render(request, 'administrative/beneficiary.html', context)


def load_communities(request):
    promoter_id = request.GET.get('promoter')
    communities = Promoter.objects.get(id=promoter_id).communities.all()
    return render(request, 'administrative/community_dropdown_list.html', {'communities':communities})

@login_required
def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if all([form.is_valid()]):
            beneficiary = Beneficiary   (
                                        name=form.cleaned_data['name'],
                                        last_name_paternal=form.cleaned_data['last_name_paternal'],
                                        last_name_maternal=form.cleaned_data['last_name_maternal'],
                                        num_of_family_beneficiaries=form.cleaned_data['num_of_family_beneficiaries'],
                                        contact_name=form.cleaned_data['contact_name'],
                                        contact_phone=form.cleaned_data['contact_phone'],
                                        account_number=form.cleaned_data['account_number'],
                                        bank_name=form.cleaned_data['bank_name'],
                                        promoter=form.cleaned_data['promoter'][0],
                                        community=form.cleaned_data['community'][0]
                                        )

            beneficiary.save()

            if not form.cleaned_data['water_capacity']:
                water_capacity = 0
            else:
                water_capacity = form.cleaned_data['water_capacity']

            beneficiary_in_program = BeneficiaryInProgram(
                                                        beneficiary=beneficiary,
                                                        program=form.cleaned_data['member_in'][0],
                                                        curp=form.cleaned_data['curp'],
                                                        house_address=form.cleaned_data['house_address'],
                                                        house_references=form.cleaned_data['house_references'],
                                                        huerto_coordinates=form.cleaned_data['huerto_coordinates'],
                                                        water_capacity=water_capacity,
                                                        savings_account_role=form.cleaned_data['savings_account_role']
                                                        )
            beneficiary_in_program.save()
            return HttpResponseRedirect('/administrative/beneficiaries/0')
        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")

    elif request.method == 'GET':
        form = BeneficiaryForm()
        context = {'form': form}
        return render(request, 'administrative/new_beneficiary.html', context)

@login_required
def modify_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryInProgramForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['water_capacity']:
                water_capacity = 0
            else:
                water_capacity = form.cleaned_data['water_capacity']

            beneficiary = form.cleaned_data['beneficiary'][0]
            beneficiary_in_program = BeneficiaryInProgram(
                                                        beneficiary=beneficiary,
                                                        program=form.cleaned_data['program'][0],
                                                        curp=form.cleaned_data['curp'],
                                                        house_address=form.cleaned_data['house_address'],
                                                        house_references=form.cleaned_data['house_references'],
                                                        huerto_coordinates=form.cleaned_data['huerto_coordinates'],
                                                        water_capacity=water_capacity,
                                                        savings_account_role=form.cleaned_data['savings_account_role']
                                                        )
            beneficiary_in_program.save()

            return HttpResponseRedirect('/administrative/beneficiaries/'+ str(beneficiary.id))
        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")

@login_required
def communities(request):
    #Description: Renders the view to register a new community on the system, when posted stores the data
    #Parameters: request
    #Function return expected: For POST request: redirect, For GET request: render
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = Community(  name=form.cleaned_data['name'],
                                    state=form.cleaned_data['state'],
                                    municipality=form.cleaned_data['municipality'],
                                 )
            community.save()
            return HttpResponseRedirect('/administrative/communities/')
    elif request.method == 'GET':
        community_form = CommunityForm()
        context = {'community_form': community_form}
        return render(request, 'administrative/communities.html', context)

@login_required
def weekly_sessions(request):
    if request.method == 'POST':
        form = WeeklySessionForm(request.POST, request.FILES)
        evidences = request.FILES.getlist('evidence')
        #print("\n\n\n getlist('evidence')" + str(request.FILES.getlist('evidence')))
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

            print("\n\n\n newSession.id = " + str(newSession.id))
            for e in evidences:
                newEvidence = WeeklySessionEvidence(
                                                    weekly_session = newSession,
                                                    evidence = e
                                                    )
                newEvidence.save()

            return HttpResponseRedirect('/administrative/weekly_sessions/')
        else:
            print("-------------------")
            print("Form is not valid")
            print(form.errors)
    else:
        if is_promoter(request.user):
            base_user = BaseUser.objects.get(user = request.user.id)
            promoter = Promoter.objects.get(base_user = base_user.id)

            beneficiaries = Beneficiary.objects.filter(promoter=promoter)

            weekly_session_form = WeeklySessionForm()
            context = {'weekly_session_form': weekly_session_form, 'beneficiaries': beneficiaries}
            return render(request, 'administrative/weekly_sessions.html', context)
        else:
            weekly_sessions = WeeklySession.objects.filter().order_by('-created_at')

            for session in weekly_sessions:
                session.assistant_count = session.assistants.all().count()

            context = {'weekly_sessions': weekly_sessions}
            return render(request, 'administrative/Admin_weekly_sessions.html', context)

@login_required
def get_weekly_session(request, pk):
    if request.method == 'GET':
        weekly_session = WeeklySession.objects.get(pk=pk)
        promoter = "" + str(weekly_session.promoter)

        assistants = weekly_session.assistants.all()
        assistantJSON = ""
        for assistant in assistants:
            assistantJSON += assistant.name + " " + assistant.last_name_paternal + ","
        assistantJSON = assistantJSON[:-1]

        evidences = WeeklySessionEvidence.objects.filter(weekly_session_id = pk)
        evidenceJSON = ""
        for eviden in evidences:
            evidence_add = eviden.evidence.url.split("_evidence/").pop()
            evidenceJSON += evidence_add + ","
        evidenceJSON = evidenceJSON[:-1]

        json_session =  {
                            'pk': weekly_session.pk,
                            'promoter': promoter,
                            'type': weekly_session.type,
                            'topic': weekly_session.topic,
                            'date': weekly_session.created_at,
                            'start': weekly_session.start_time,
                            'end': weekly_session.end_time,
                            #'assistants': serializers.serialize('json', weekly_session.assistants.all())
                            'assistants': assistantJSON,
                            'evidences': evidenceJSON
                        }
        return JsonResponse(json_session)

@login_required
def payments(request, pk=0):
    if request.method == 'GET':
        if is_promoter(request.user):
            #A promoter wants to check their payments
            base_user = BaseUser.objects.get(user = request.user.id)
            promoter = Promoter.objects.get(base_user = base_user.id)

            upcoming_payments = Payment.objects.filter(promoter=promoter, pay_date__isnull=True).order_by('due_date')
            past_payments = Payment.objects.filter(promoter=promoter, pay_date__isnull=False).order_by('-due_date')

            context = {'upcoming_payments': upcoming_payments, 'past_payments': past_payments}
            return render(request, 'administrative/payments.html', context)
        else:
            #An administrative user wants to check promoters payments.
            upcoming_payments = Payment.objects.filter(pay_date__isnull=True).order_by('due_date')
            past_payments = Payment.objects.filter(pay_date__isnull=False).order_by('-due_date')
            curdate = timezone.now()
            form = PayForm()
            context = {
                        'upcoming_payments': upcoming_payments,
                        'past_payments': past_payments,
                        'curdate':curdate,
                        'form':form
                        }
            return render(request, 'administrative/Admin_payments.html', context)
    elif request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.get(pk=pk)
            time = timezone.now()
            payment.pay_date=time
            payment.comment=form.cleaned_data['comment']
            payment.updated_at=time
            payment.save()
        else:
            messages.warning(request,'Favor de llenar los campos.')
        upcoming_payments = Payment.objects.filter(pay_date__isnull=True).order_by('due_date')
        past_payments = Payment.objects.filter(pay_date__isnull=False).order_by('-due_date')
        curdate = timezone.now()
        form = PayForm()
        context = {
                    'upcoming_payments': upcoming_payments,
                    'past_payments': past_payments,
                    'curdate':curdate,
                    'form':form
                    }
        return render(request, 'administrative/Admin_payments.html', context)

@login_required
def get_payment(request, pk):
    """
    Description: Gets the information of a specific payment
    Parameters: request, pk -> the id of the specific payment
    Return: Json containing the payment information
    """
    if request.method == 'GET':
        payment = Payment.objects.get(pk=pk)
        promoter = "" + str(payment.promoter)
        json_payment =  {
                            'pk': payment.pk,
                            'promoter': promoter,
                            'description': payment.description,
                            'quantity': payment.quantity
                        }
        return JsonResponse(json_payment)

@login_required
def alert_list(request):
    """
    Description: Renders a list of alerts
    Parameters: request
    Return: Render
    """
    if request.method == 'GET':
        solved_alerts = HelpAlert.objects.exclude(resolved_at__isnull=True)
        pending_alerts = HelpAlert.objects.filter(resolved_at__isnull=True)
        return render(request, 'administrative/alert_list.html', {'solved_alerts': solved_alerts, 'pending_alerts': pending_alerts})

@login_required
def resolve_alert(request, pk):
    """
    Description: Updates an alert, setting the resolved_at time to now, as well
    as the updated_at date.
    Parameters: pk -> id of the alert to be modified
    Returns: HttpResponseRedirect to the alerts page
    """
    alert = HelpAlert.objects.get(pk=pk)
    alert.resolved_at=timezone.now()
    alert.updated_at=timezone.now()
    alert.save()
    return HttpResponseRedirect('/administrative/alerts/')

@login_required
def add_saving_account(request):
    if request.method == 'POST':
        form = SavingAccountForm(request.POST)
        if form.is_valid():
            print("-----------------------------")
            print("form is valid")
            print("-----------------------------")
            saving_account = SavingAccount(
                                    name=form.cleaned_data['name'],
                                    community=form.cleaned_data['community'],
                                    municipality=form.cleaned_data['municipality'],
                                    location=form.cleaned_data['location'],
                                    total_saved_amount=form.cleaned_data['total_saved_amount'],
                                    president_beneficiary=form.cleaned_data['president_beneficiary'][0],
                                    treasurer_beneficiary=form.cleaned_data['treasurer_beneficiary'][0],
                                    partner_beneficiary=form.cleaned_data['partner_beneficiary'][0]
                                )
            saving_account.save()
            saving_account.list_of_beneficiaries.set(form.cleaned_data['list_of_beneficiaries'])
            saving_account.save()
            return HttpResponseRedirect('/administrative/')
        else:

            print("-----------------------------")
            print("form is not valid")
            print(form.errors)
            print("-----------------------------")
    elif request.method == 'GET':
        form = SavingAccountForm()
        context = {'form': form}
        return render(request, 'administrative/new_saving_account.html', context)

def training_session(request):
    """
    Description: Handles the creation and rendering of training sessions
    Parameters: request
    Returns: Render
    """
    if request.method == 'POST':
        date = request.POST['date']
        date_obj = datetime.strptime(date, "%d-%m-%Y")
        data = {
                    'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                    'topic': request.POST['topic'],
                    'date': date_obj,
                    'start_time':request.POST['start_time'],
                    'end_time':request.POST['end_time'],
                    'comments': request.POST['comments'],
                    'assistants': request.POST.getlist("assistants")
                }
        form = TrainingForm(data, request.FILES)
        print("evidence: " + str(request.FILES.getlist('evidence')))
        images = request.FILES.getlist('evidence')
        if form.is_valid():
            base_user = BaseUser.objects.get(user=request.user)
            session = TrainingSession   (
                                            topic=form.cleaned_data['topic'],
                                            trainer=base_user,
                                            date=form.cleaned_data['date'],
                                            start_time=form.cleaned_data['start_time'],
                                            end_time=form.cleaned_data['end_time'],
                                            comments=form.cleaned_data['comments']
                                        )
            session.save()
            assistants = request.POST.getlist("assistants")
            session.assistants.set(assistants)
            for evidence in images:
                ev = TrainingSessionEvidence (
                                                training_session = session,
                                                evidence = evidence
                                            )
                ev.save()
        else:
            print(form.errors)
            messages.warning(request,'Hubo errores en la forma, intente de nuevo')
    form = TrainingForm()
    curdate = timezone.now()
    return render(request, 'administrative/training_sessions.html', {'form':form, 'curdate': curdate})
