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
def fill_Production_Report(request):
    return render(request, 'administrative/Production_Report.html')

def add_beneficiary(request):
    if request.method == 'GET':
        #form =
        context = {'form': form}
        return render(request, 'path/to/tempate.html', context)

@login_required
def weekly_sessions(request):
    if request.method == 'POST':
        form = WeeklySessionForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
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
