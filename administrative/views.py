"""
Created by: Django
Description: Functions for handling requests to the server
Modified by: Bernardo, Hugo, Alex, Francisco
Modify date: 19/10/2018
"""

from django import template
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Func, F
from profiles.models import HelpAlert
from django.http import Http404
from .models import *
from .forms import *
from datetime import datetime, time
from django.utils import formats

#Helper functions
def is_promoter(user):
    #Description: Check if a user is a promoter
    #Parameter: user
    #Return: boolean indicating wheter the user is a promoter
    base = BaseUser.objects.get(user=user)
    try:
        promoter = Promoter.objects.get(base_user=base)
    except Promoter.DoesNotExist:
        return False
    return True

def is_director(user):
    #Description: Check if a user is a director
    #Parameter: user
    #Return: True if user is director
    if user:
        return user.groups.filter(name='Director').count() == 1
    return False

def is_trainer(user):
    #Description: Check if a user is a trainer
    #Parameter: user
    #Return: True if user is trainer
    if user:
        return user.groups.filter(name='Capacitador').count() == 1
    return False

def is_administrative_assistant(user):
    #Description: Check if a user is an administrative assistant
    #Parameter: user
    #Return: True if user is an administrative assistant
    if user:
        return user.groups.filter(name='Asistente Administrativo').count() == 1
    return False

def is_administrative_coordinator(user):
    #Description: Check if a user is an administrative coordinator
    #Parameter: user
    #Return: True if user is an administrative coordinator
    if user:
        return user.groups.filter(name='Coordinador Administrativo').count() == 1
    return False

def is_field_technician(user):
    #Description: Check if a user is a field technician
    #Parameter: user
    #Return: True if user is a field technician
    if user:
        return user.groups.filter(name='Técnico de Campo').count() == 1
    return False

def is_counter(user):
    if user:
        return user.groups.filter(name='Contador').count() == 1
    return False

# Create your views here.
@login_required
def index(request):
    if is_promoter(request.user):
        base = BaseUser.objects.get(user=request.user)
        try:
            promoter = Promoter.objects.get(base_user=base)
        except Promoter.DoesNotExist:
            return render(request, 'administrative/index/promoter.html')

        return render(request, 'administrative/index/promoter.html', {'promoterId': promoter.id})
    else:
        return render(request, 'administrative/index.html')
    return


@login_required
def production_report(request):
    """
        Description: Renders the view to register a new productionn report on the system, when posted stores the data
        Parameters: request
        return: For POST request: redirect, For GET request: render
    """
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
            if not form.cleaned_data['beneficiary']:
                beneficiary = Beneficiary.objects.get(id=1)
            else:
                beneficiary = form.cleaned_data['beneficiary'][0]

            newProductionReport = ProductionReport(

                                                    beneficiary = beneficiary,
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
    elif request.method == 'GET':
        if is_promoter(request.user):
            production_report_form = ProductionReportForm()
            base = BaseUser.objects.get(user=request.user)
            promoter = Promoter.objects.get(base_user=base)
            beneficiaries = Beneficiary.objects.filter(promoter=promoter)
            context = {'production_report_form': production_report_form, 'beneficiaries': beneficiaries}
            return render(request, 'administrative/Production_Report.html', context)
        else:
            return HttpResponseRedirect('/administrative/production_report_list/')
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def production_report_list(request):
    if request.method == 'GET':
        if is_promoter(request.user):
            review_reports_unfiltered = ProductionReport.objects.exclude(exch_seed=0).filter(get_for_seed_qty=0).exclude(paid=True) | ProductionReport.objects.exclude(exch_leaf=0).filter(get_for_leaf_qty=0).exclude(paid=True)
            pending_reports_unfiltered = ProductionReport.objects.exclude(paid=True).exclude(get_for_seed_qty=0) | ProductionReport.objects.exclude(paid=True).exclude(get_for_leaf_qty=0)#.exclude(get_for_seed_qty=0) | ProductionReport.objects.exclude(get_for_leaf_qty=0)
            paid_reports_unfiltered = ProductionReport.objects.filter(paid=True)
            base = BaseUser.objects.get(user=request.user)
            promoter = Promoter.objects.get(base_user=base)
            beneficiaries = Beneficiary.objects.filter(promoter=promoter)

            review_reports = []
            pending_reports = []
            paid_reports = []
            for beneficiary in beneficiaries:
                review_reports.extend(review_reports_unfiltered.filter(beneficiary=beneficiary))
                pending_reports.extend(pending_reports_unfiltered.filter(beneficiary=beneficiary))
                paid_reports.extend(paid_reports_unfiltered.filter(beneficiary=beneficiary))

            return render(request, 'administrative/production_report_list.html', {'review_reports': review_reports, 'paid_reports': paid_reports, 'pending_reports': pending_reports})
        else:
            review_reports = ProductionReport.objects.exclude(exch_seed=0).filter(get_for_seed_qty=0).exclude(paid=True) | ProductionReport.objects.exclude(exch_leaf=0).filter(get_for_leaf_qty=0).exclude(paid=True)
            pending_reports = ProductionReport.objects.exclude(paid=True).exclude(get_for_seed_qty=0) | ProductionReport.objects.exclude(paid=True).exclude(get_for_leaf_qty=0)#.exclude(get_for_seed_qty=0) | ProductionReport.objects.exclude(get_for_leaf_qty=0)
            paid_reports = ProductionReport.objects.filter(paid=True)
            return render(request, 'administrative/production_report_list.html', {'review_reports': review_reports, 'paid_reports': paid_reports, 'pending_reports': pending_reports})


@login_required
def administrative_production_report(request, pk):
    if request.method == 'GET':

        try:
            production_report = ProductionReport.objects.get(pk=pk)
        except ProductionReport.DoesNotExist:
            raise Http404("No existe ese Reporte de Producción.")

        production_report_form = ProductionReportForm()

        if is_promoter(request.user):
            return render(request, 'administrative/promoter_production_report.html', {'prod_report': production_report, 'production_report_form': production_report_form})
        else:
            return render(request, 'administrative/administrative_production_report.html', {'prod_report': production_report, 'production_report_form': production_report_form})
    elif request.method == 'POST':
        try:
            production_report = ProductionReport.objects.get(pk=pk)
        except ProductionReport.DoesNotExist:
            raise Http404("No existe ese Reporte de Producción.")

        data = request.POST
        print(data)

        if 'get_for_leaf_qty' in data:
            if data['get_for_leaf_qty'] != '':
                production_report.get_for_leaf_qty = data['get_for_leaf_qty']

        if 'get_for_seed_qty' in data:
            if data['get_for_seed_qty'] != '':
                production_report.get_for_seed_qty = data['get_for_seed_qty']
        if 'paid' in data:
            production_report.paid = data['paid']

        if 'want_for_leaf' in data:
            production_report.want_for_leaf = data['want_for_leaf']
        if 'want_for_seed' in data:
            production_report.want_for_seed = data['want_for_seed']

        if 'exch_leaf' in data:
            production_report.exch_leaf = data['exch_leaf']
        if 'exch_seed' in data:
            production_report.exch_seed = data['exch_seed']

        production_report.save()
        return HttpResponseRedirect('/administrative/production_report_list/')

@login_required
def beneficiaries_list(request):
    return HttpResponseRedirect('/administrative/beneficiaries/0')

@login_required
def beneficiaries(request, pk):
    if request.method == 'GET':
        not_promoter = not is_promoter(request.user)

        if pk == 0:
            beneficiaries = Beneficiary.objects.all()
            if is_promoter(request.user):
                base = BaseUser.objects.get(user=request.user)
                promoter = Promoter.objects.get(base_user=base)
                beneficiaries = Beneficiary.objects.filter(promoter=promoter)
            return render(request, 'administrative/beneficiaries.html', {'beneficiaries': beneficiaries, 'not_promoter': not_promoter})
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

            context = {'form': form, 'beneficiary': beneficiary, 'programs': programs, 'allowed_programs': allowed_programs, 'not_promoter': not_promoter}
            return render(request, 'administrative/beneficiary.html', context)

@login_required
def load_communities(request):
    promoter_id = request.GET.get('promoter')
    communities = Promoter.objects.get(id=promoter_id).communities.all()
    return render(request, 'administrative/community_dropdown_list.html', {'communities':communities})

@login_required
def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            beneficiary = Beneficiary   (
                                        name=form.cleaned_data['name'],
                                        last_name_paternal=form.cleaned_data['last_name_paternal'],
                                        last_name_maternal=form.cleaned_data['last_name_maternal'],
                                        phone=form.cleaned_data['phone'],
                                        email=form.cleaned_data['email'],
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
                                                        savings_account_role=form.cleaned_data['savings_account_role'],
                                                        cisterna_location = form.cleaned_data['cisterna_location'],
                                                        cisterna_status = form.cleaned_data['cisterna_status'],
                                                        school = form.cleaned_data['school'],
                                                        age = form.cleaned_data['age'],
                                                        initial_weight = form.cleaned_data['initial_weight']

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
        if is_promoter(request.user):
            return HttpResponseRedirect('/administrative/')
        else:
            form = BeneficiaryForm()
            context = {'form': form}
            return render(request, 'administrative/new_beneficiary.html', context)

@login_required
def edit_beneficiary(request,pk):
    """ Description: Edits the information of a beneficiary
        Parameters: request, pk of the beneficiary that is edited
        return: render
    """
    if not (is_promoter(request.user)):
        if request.method == 'POST':
            form = EditBeneficiaryForm(data=request.POST)

            if form.is_valid():
                beneficiary = Beneficiary.objects.get(id=pk)

                beneficiary.name=form.cleaned_data['name']
                beneficiary.last_name_paternal=form.cleaned_data['last_name_paternal']
                beneficiary.last_name_maternal=form.cleaned_data['last_name_maternal']
                beneficiary.phone=form.cleaned_data['phone']
                beneficiary.email=form.cleaned_data['email']
                beneficiary.num_of_family_beneficiaries=form.cleaned_data['num_of_family_beneficiaries']
                beneficiary.account_number=form.cleaned_data['account_number']
                beneficiary.bank_name=form.cleaned_data['bank_name']
                beneficiary.contact_name=form.cleaned_data['contact_name']
                beneficiary.contact_phone=form.cleaned_data['contact_phone']
                beneficiary.promoter=form.cleaned_data['promoter'][0]
                beneficiary.community=form.cleaned_data['community'][0]
                beneficiary.updated_at=timezone.now()

                beneficiary.save()

                return HttpResponseRedirect('/administrative/beneficiaries/')
        else:
            beneficiary = Beneficiary.objects.get(id=pk)

            form = EditBeneficiaryForm()

            context = {'beneficiary': beneficiary, 'form': form}
            return render(request, 'administrative/edit_beneficiary.html', context)
    else:
        return HttpResponseRedirect('/administrative/beneficiaries/')

@login_required
def remove_from_program(request, p_id):
    if request.method == 'GET':
        b_in_p = BeneficiaryInProgram.objects.get(id=p_id)
        print(b_in_p)

        b_in_p.delete()

        return HttpResponseRedirect('/administrative/beneficiaries/')

@login_required
def modify_beneficiary(request):
    print(request.POST)
    if request.method == 'POST':
        form = BeneficiaryInProgramForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['water_capacity']:
                water_capacity = 0
            else:
                water_capacity = form.cleaned_data['water_capacity']

            if not form.cleaned_data['age']:
                age = 0
            else:
                age = form.cleaned_data['age']

            if not form.cleaned_data['initial_weight']:
                initial_weight = 0
            else:
                initial_weight = form.cleaned_data['initial_weight']

            print(age)
            beneficiary = form.cleaned_data['beneficiary'][0]
            beneficiary_in_program = BeneficiaryInProgram(
                                                        beneficiary=beneficiary,
                                                        program=form.cleaned_data['program'][0],
                                                        curp=form.cleaned_data['curp'],
                                                        house_address=form.cleaned_data['house_address'],
                                                        house_references=form.cleaned_data['house_references'],
                                                        huerto_coordinates=form.cleaned_data['huerto_coordinates'],
                                                        water_capacity=water_capacity,
                                                        savings_account_role=form.cleaned_data['savings_account_role'],
                                                        cisterna_location = form.cleaned_data['cisterna_location'],
                                                        cisterna_status = form.cleaned_data['cisterna_status'],
                                                        school = form.cleaned_data['school'],
                                                        age = age,
                                                        initial_weight = initial_weight
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
    """ Description: Renders the view to register a new community on the system, when posted stores the data
        Parameters: request
        return: For POST request: redirect, For GET request: render
    """
    if not (is_promoter(request.user)):
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
            communities = Community.objects.all()
            context = {'community_form': community_form, 'communities': communities}
            return render(request, 'administrative/communities.html', context)
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def my_communities(request):
    if is_promoter(request.user):
        if request.method == 'GET':
            base = BaseUser.objects.get(user=request.user)
            promoter = Promoter.objects.get(base_user=base)
            comms = promoter.communities.all()
            communities = []
            for community in comms:
                communities.append({
                    'data': community,
                    'beneficiaries': Beneficiary.objects.filter(community=community)
                })
            print(communities)
            return render(request, 'administrative/promoter_communities.html', {'communities': communities})
        else:
            return HttpResponseRedirect('/administrative/')
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def weekly_sessions(request):
    """ Description: Renders the view of weekly sessions for each role
        Parameters: request
        return: For POST request: redirect, For GET request: render
    """
    if(is_promoter(request.user)):
        if request.method == 'POST':
            date = request.POST['date']
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            data = {
                        'date': date_obj,
                        'type': request.POST['type'],
                        'topic': request.POST['topic'],
                        'start_time':request.POST['start_time'],
                        'end_time':request.POST['end_time'],
                        'assistants': request.POST.getlist("assistants")
                    }
            form = WeeklySessionForm(data, request.FILES)
            evidences = request.FILES.getlist('evidence')

            if form.is_valid():
                base_user = BaseUser.objects.get(user = request.user.id)
                promoter = Promoter.objects.get(base_user = base_user.id)
                newSession = WeeklySession(
                                            promoter=promoter,
                                            date=form.cleaned_data['date'],
                                            type=form.cleaned_data['type'],
                                            topic=form.cleaned_data['topic'],
                                            start_time=form.cleaned_data['start_time'],
                                            end_time=form.cleaned_data['end_time'],
                                           )
                newSession.save()

                list = request.POST.getlist("assistants")
                for assistant in list:
                    newSession.assistants.add(Beneficiary.objects.get(id = assistant))

                for e in evidences:
                    newEvidence = WeeklySessionEvidence(
                                                        weekly_session = newSession,
                                                        evidence = e
                                                        )
                    newEvidence.save()

                return HttpResponseRedirect('/administrative/weekly_sessions/')
        else:
            base_user = BaseUser.objects.get(user = request.user.id)
            promoter = Promoter.objects.get(base_user = base_user.id)

            beneficiaries = Beneficiary.objects.filter(promoter=promoter)

            weekly_session_form = WeeklySessionForm()
            #Existing sessions
            weekly_sessions = WeeklySession.objects.filter(promoter=promoter).order_by('-date')

            for session in weekly_sessions:
                session.assistant_count = session.assistants.all().count()

            context = {'weekly_session_form': weekly_session_form, 'beneficiaries': beneficiaries, 'weekly_sessions': weekly_sessions}
            return render(request, 'administrative/weekly_sessions.html', context)
    elif(is_administrative_assistant(request.user) | is_administrative_coordinator(request.user)):
        weekly_sessions = WeeklySession.objects.filter().order_by('-date')

        for session in weekly_sessions:
            session.assistant_count = session.assistants.all().count()

        context = {'weekly_sessions': weekly_sessions}
        return render(request, 'administrative/Admin_weekly_sessions.html', context)
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def edit_weekly_session(request,pk):
    """ Description: Edits the information of a weekly session
        Parameters: request, pk of the session that is edited
        return: render
    """
    if (is_promoter(request.user)):
        if request.method == 'POST':
            date = request.POST['date']
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            data = {
                        'date': date_obj,
                        'type': request.POST['type'],
                        'topic': request.POST['topic'],
                        'start_time':request.POST['start_time'],
                        'end_time':request.POST['end_time'],
                        'assistants': request.POST.getlist("assistants")
                    }
            form = WeeklySessionForm(data, request.FILES)
            evidences = request.FILES.getlist('evidence')

            existing_evidences_keep = request.POST.getlist('image_keep')
            existing_evidences_total = request.POST.getlist('image_total')

            if form.is_valid():
                session = WeeklySession.objects.get(id=pk)

                session.date=form.cleaned_data['date']
                session.type=form.cleaned_data['type']
                session.topic=form.cleaned_data['topic']
                session.start_time=form.cleaned_data['start_time']
                session.end_time=form.cleaned_data['end_time']

                session.save()

                list = request.POST.getlist("assistants")
                session.assistants.clear()
                for assistant in list:
                    session.assistants.add(Beneficiary.objects.get(id = assistant))

                all_evidences = WeeklySessionEvidence.objects.filter(weekly_session_id = pk)

                for e in existing_evidences_keep:
                    e = int(e)

                for e in existing_evidences_total:
                    e = int(e)

                existing_evidences_total = set(existing_evidences_total) - set(existing_evidences_keep)

                all_evidences_list = []
                for e in all_evidences:
                    all_evidences_list.append(e.id)

                for e in all_evidences_list:
                    for evi in existing_evidences_total:
                        if (int(e) == int(evi)):
                            deleted_evidence = WeeklySessionEvidence.objects.filter(id = evi)
                            deleted_evidence.delete()

                for e in evidences:
                    newEvidence = WeeklySessionEvidence(
                                                        weekly_session = session,
                                                        evidence = e
                                                        )
                    newEvidence.save()

                return HttpResponseRedirect('/administrative/weekly_sessions/')
        else:
            session = WeeklySession.objects.get(id=pk)

            base_user = BaseUser.objects.get(user = request.user.id)
            promoter = Promoter.objects.get(base_user = base_user.id)

            beneficiaries = Beneficiary.objects.filter(promoter=promoter)

            weekly_session_form = WeeklySessionForm()

            assistants = session.assistants.all()

            date = formats.date_format(session.date, "d-m-Y")

            evidences = WeeklySessionEvidence.objects.filter(weekly_session_id = pk)

            context = {'session': session, 'weekly_session_form': weekly_session_form, 'beneficiaries': beneficiaries, 'assistants': assistants, 'date': date, 'evidences': evidences}
            return render(request, 'administrative/edit_weekly_session.html', context)
    else:
        return HttpResponseRedirect('/administrative/weekly_sessions/')

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
                            'date': weekly_session.date,
                            'start': weekly_session.start_time,
                            'end': weekly_session.end_time,
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
            new_payment = PaymentForm()
            context = {
                        'upcoming_payments': upcoming_payments,
                        'past_payments': past_payments,
                        'curdate':curdate,
                        'form':form,
                        'new_payment': new_payment
                        }
            return render(request, 'administrative/Admin_payments.html', context)
    elif request.method == 'POST':
        if not is_promoter(request.user):
            form = PayForm(request.POST)
            if form.is_valid():
                print('paying')
                payment = Payment.objects.get(pk=pk)
                time = timezone.now()
                payment.pay_date=time
                payment.comment=form.cleaned_data['comment']
                payment.updated_at=time
                payment.save()
                print(payment.comment)
            else:
                print('not paying')
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
        else:
            return HttpResponseRedirect('/administrative/')

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
def add_payment(request):
    """
    Description: Creates a new payment
    Return: HttpResponseRedirect
    """
    if not is_promoter(request.user):
        if request.method == 'POST':
            date = request.POST['due_date']
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            data = {
                        'promoter': request.POST['promoter'],
                        'due_date': date_obj,
                        'description':request.POST['description'],
                        'quantity':request.POST['quantity'],
                    }

            form = PaymentForm(data)
            if form.is_valid():
                new_payment = Payment(
                                    promoter=form.cleaned_data['promoter'],
                                    description=form.cleaned_data['description'],
                                    quantity=form.cleaned_data['quantity'],
                                    due_date=form.cleaned_data['due_date']
                                    )
                new_payment.save()
            else:
                messages.warning(request,'No se pudo registrar el pago, intente de nuevo')
                print("-------------------")
                print("\n\n\n\n\n")
                print("Form is not valid")
                print(form.errors)
                print("\n\n\n\n\n")
            return HttpResponseRedirect('/administrative/payments/')
    return HttpResponseRedirect('/administrative/')

@login_required
def alert_list(request):
    """
    Description: Renders a list of alerts
    Parameters: request
    Return: Render
    """
    if not is_promoter(request.user):
        if request.method == 'GET':
            solved_alerts = HelpAlert.objects.exclude(resolved_at__isnull=True)
            pending_alerts = HelpAlert.objects.filter(resolved_at__isnull=True)
            return render(request, 'administrative/alert_list.html', {'solved_alerts': solved_alerts, 'pending_alerts': pending_alerts})
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def resolve_alert(request, pk):
    """
    Description: Updates an alert, setting the resolved_at time to now, as well
    as the updated_at date.
    Parameters: pk -> id of the alert to be modified
    Returns: HttpResponseRedirect to the alerts page
    """
    if not is_promoter(request.user):
        alert = HelpAlert.objects.get(pk=pk)
        alert.resolved_at=timezone.now()
        alert.updated_at=timezone.now()
        alert.save()
    return HttpResponseRedirect('/administrative/')

@login_required
def saving_accounts(request):
    """
    Description: List saving accounts
    Parameters: request
    Return: Render
    """
    u = request.user
    # Validate user type
    if is_field_technician(u) or is_administrative_assistant(u) or is_administrative_coordinator(u):
        if request.method == 'GET':
            account_list = SavingAccount.objects.filter(deleted_at__isnull=True).order_by('municipality')
            context = {'account_list':account_list}
            return render(request, 'administrative/saving_accounts.html', context)

    return HttpResponseRedirect('/administrative/')

@login_required
def edit_savings(request, pk=0):
    """
    Description: Edits a savings account and the corresponding SavingsLog Object
    Parameters: request, pk of the account being edited
    return: render or HttpResponseRedirect
    """
    u = request.user
    # Validate user type
    if is_field_technician(u) or is_administrative_assistant(u) or is_administrative_coordinator(u):
        form = UpdateSavingsForm()
        if request.method == 'POST':
            form = UpdateSavingsForm(request.POST)
            if form.is_valid():
                account_id = form.cleaned_data['pk']
                if request.POST['transaction_type'] == 'deposit':
                    amount = form.cleaned_data['amount']
                else:
                    amount =  0 - form.cleaned_data['amount']
                #Savings Account object
                account = SavingAccount.objects.get(pk=account_id)
                account.total_saved_amount = account.total_saved_amount + amount
                account.name = form.cleaned_data['name']
                account.community = form.cleaned_data['community']
                account.municipality = form.cleaned_data['municipality']
                account.location = form.cleaned_data['location']
                account.list_of_beneficiaries.set(form.cleaned_data['list_of_beneficiaries'])
                account.president_beneficiary = form.cleaned_data['president_beneficiary']
                account.treasurer_beneficiary = form.cleaned_data['treasurer_beneficiary']
                account.updated_at = timezone.now()
                account.save()
                #SavingsLog object
                month = datetime.now().month
                year = datetime.now().year
                log = SavingsLog.objects.get_or_create(saving_account=account, month=month, year=year)
                log.amount = account.total_saved_amount
                log.save()
                return HttpResponseRedirect('/administrative/saving_accounts/')
            else:
                return HttpResponseRedirect('/administrative/edit_savings/'+request.POST['pk']+'/')
        else:
            account = get_object_or_404(SavingAccount, pk=pk)
            current_beneficiaries = account.list_of_beneficiaries.all()
            context = {'form': form, 'account': account, 'current_beneficiaries':current_beneficiaries}
            return render(request, 'administrative/edit_savings.html', context)
    return HttpResponseRedirect('/administrative/saving_accounts/')

@login_required
def add_saving_account(request):
    """
    Description: Creates a new saving account and saves to DB
    Parameters: request
    Return: Redirect
    """
    if (is_administrative_assistant(request.user) | is_administrative_coordinator(request.user) | is_field_technician(request.user)):
        if request.method == 'POST':
            form = SavingAccountForm(request.POST)
            if form.is_valid():
                saving_account = SavingAccount(
                                        name=form.cleaned_data['name'],
                                        community=form.cleaned_data['community'][0],
                                        municipality=form.cleaned_data['municipality'],
                                        location=form.cleaned_data['location'],
                                        total_saved_amount=form.cleaned_data['total_saved_amount'],
                                        president_beneficiary=form.cleaned_data['president_beneficiary'],
                                        treasurer_beneficiary=form.cleaned_data['treasurer_beneficiary'],
                                    )
                saving_account.save()
                saving_account.list_of_beneficiaries.set(form.cleaned_data['list_of_beneficiaries'])
                saving_account.save()
                return HttpResponseRedirect('/administrative/saving_accounts/')
            else:

                print("-----------------------------")
                print("form is not valid")
                print(form.errors)
                print("-----------------------------")
        elif request.method == 'GET':
            form = SavingAccountForm()
            context = {'form': form}
            return render(request, 'administrative/new_saving_account.html', context)
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def training_session(request):
    """
    Description: Handles the creation and rendering of training sessions
    Parameters: request
    Returns: Render
    """
    if not is_promoter(request.user):
        if request.method == 'POST':
            date = request.POST['date']
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            data = {
                        'topic': request.POST['topic'],
                        'date': date_obj,
                        'start_time':request.POST['start_time'],
                        'end_time':request.POST['end_time'],
                        'comments': request.POST['comments'],
                        'assistants': request.POST.getlist("assistants")
                    }
            form = TrainingForm(data, request.FILES)
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
        training_session_list = TrainingSession.objects.order_by('date')
        return render(request, 'administrative/training_sessions.html', {'form':form, 'curdate': curdate, 'training_session_list':training_session_list})
    else:
        return HttpResponseRedirect('/administrative/')

def edit_training_session(request, pk):
    """
    Description: Edits a training session and updates information
    Parameters: request, pk of the account being edited
    return: render or HttpResponseRedirect
    """
    u = request.user
    base_user = BaseUser.objects.get(user_id=u.id)
    # Validate user type
    if not is_promoter(u):
        form = UpdateTrainingForm()
        if request.method == 'POST':
            form = UpdateTrainingForm(request.POST)
            date = request.POST['date']
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            data = {
                        'topic': request.POST['topic'],
                        'date': date_obj,
                        'start_time':request.POST['start_time'],
                        'end_time':request.POST['end_time'],
                        'comments': request.POST['comments'],
                        'assistants': request.POST.getlist("assistants")
                    }
            form = UpdateTrainingForm(data, request.FILES)
            evidences = request.FILES.getlist('evidence')
            existing_evidences_keep = request.POST.getlist('image_keep')
            existing_evidences_total = request.POST.getlist('image_total')
            if form.is_valid():
                #Training Session object
                session = TrainingSession.objects.get(pk=pk)
                # training_session_evidence = get_object_or_404(TrainingSessionEvidence,training_session_id = pk)
                session.topic=form.cleaned_data['topic']
                session.trainer=base_user
                session.date= form.cleaned_data['date']
                session.start_time=form.cleaned_data['start_time']
                session.end_time=form.cleaned_data['end_time']
                session.comments=form.cleaned_data['comments']
                session.assistants.set(form.cleaned_data['assistants'])
                session.save()

                imagen = form.cleaned_data['evidence']
                print(imagen)

                # images = request.FILES.getlist('evidence')
                all_evidences =  TrainingSessionEvidence.objects.filter(training_session_id = pk)


                for e in existing_evidences_keep:
                    e = int(e)

                for e in existing_evidences_total:
                    e = int(e)

                existing_evidences_total = set(existing_evidences_total) - set(existing_evidences_keep)

                all_evidences_list = []
                for e in all_evidences:
                    all_evidences_list.append(e.id)

                # print(all_evidences_list)

                for e in all_evidences_list:
                    for evi in existing_evidences_total:
                        if (int(e) == int(evi)):
                            deleted_evidence =  TrainingSessionEvidence.objects.filter(id = evi)
                            deleted_evidence.delete()


                for e in evidences:
                    ev = TrainingSessionEvidence (
                                                    training_session = session,
                                                    evidence = e
                                                )
                    ev.save()


                return HttpResponseRedirect('/administrative/training_sessions/')

            else:
                session = get_object_or_404(TrainingSession, pk=pk)
                fecha = session.date
                # fechaString = fecha.date(fecha.year, fecha.month, fecha.day).ctime()
                fechaString = fecha.strftime("%d-%m-%Y")
                list = session.assistants.all().values_list('id', flat=True)
                evidences = TrainingSessionEvidence.objects.filter(training_session_id = pk)
                assistants = dict(zip(list[::1], list[::1]))
                messages.warning(request, 'No ha llenado todos los espacios de la forma')
                context = {'form': form, 'session': session, 'assistants':assistants, 'evidences':evidences,'fechaString':fechaString}
                return render(request, 'administrative/edit_training_session.html', context)
        else:
            session = get_object_or_404(TrainingSession, pk=pk)
            fecha = session.date
            # fechaString = fecha.date(fecha.year, fecha.month, fecha.day).ctime()
            fechaString = fecha.strftime("%d-%m-%Y")
            list = session.assistants.all().values_list('id', flat=True)
            evidences = TrainingSessionEvidence.objects.filter(training_session_id = pk)
            assistants = dict(zip(list[::1], list[::1]))
            context = {'form': form, 'session': session, 'assistants':assistants, 'evidences':evidences,'fechaString':fechaString}
            return render(request, 'administrative/edit_training_session.html', context)
    else:
        return HttpResponseRedirect('/administrative/training_sessions/')


@login_required
def community_report(request):
    if is_director(request.user):
        data = []
        municipalities = Community.objects.values('municipality').annotate(
                                                                            communities=Count('municipality'),
                                                                            promoters=Count('promoter'),
                                                                            beneficiaries=Count('beneficiary')
                                                                        )
        names = []
        promoters = []
        beneficiaries = []
        for mun in municipalities:
            data.append(mun)
            names.append(mun['municipality'])
            promoters.append(mun['promoters'])
            beneficiaries.append(mun['beneficiaries'])

        # Promoters per municipality
        context = {'dataset': data, 'names':names, 'promoters':promoters, 'beneficiaries':beneficiaries}
        return render(request, 'administrative/reports.html', context)
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def get_communities_savings(request):
    if is_director(request.user):
        savings_data = []
        municipalities = []
        curyear = timezone.now().year
        qset = Community.objects.values('municipality').annotate(d=Count('id'))
        for e in qset:
            municipalities.append(e['municipality'])
        for m in municipalities:
            qset = SavingsLog.objects.filter(saving_account__municipality=m, year=curyear).values('saving_account__municipality', 'year', 'month', 'amount').order_by('month')
            s = []
            i = 1
            for e in qset:
                while i < e['month']:
                    s.append(0)
                    i+=1
                i = 100
                s.append(float(e['amount']))
            savings_data.append(s)
        j = {
            'amounts':savings_data,
            'labels': municipalities
        }
    else:
        j = {}
    return JsonResponse(j)

@login_required
def get_communities_beneficiaries(request):
    if is_director(request.user):
        data = []
        municipalities = Community.objects.values('municipality').annotate(
                                                                            communities=Count('municipality'),
                                                                            promoters=Count('promoter'),
                                                                            beneficiaries=Count('beneficiary')
                                                                        )
        names = []
        promoters = []
        beneficiaries = []
        for mun in municipalities:
            data.append(mun)
            names.append(mun['municipality'])
            promoters.append(mun['promoters'])
            beneficiaries.append(mun['beneficiaries'])
        json_data = {
                        'labels': names,
                        'beneficiaries': beneficiaries
                    }
    else:
        json_data = {}
    return JsonResponse(json_data)

@login_required
def get_program_beneficiaries(request):
    if is_director(request.user):
        data = []
        names = []
        qset = BeneficiaryInProgram.objects.values('program').annotate(beneficiaries=Count('beneficiary'))
        print(qset)
        for p in qset:
            data.append(p['beneficiaries'])
            names.append(p['program'])
        json_data = {
                        'labels': names,
                        'beneficiaries': data
                    }
    else:
        json_data = {}
    return JsonResponse(json_data)
