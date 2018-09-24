from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *


# Create your views here.
@login_required
def index(request):
    # base_user = BaseUser.objects.get(user = request.user.id)
    # promoter = Promoter.objects.get(base_user = base_user.id)
    # print("-------------------")
    # print(promoter.id)
    alert_form = AlertForm()
    context = {'alert_form': alert_form}
    return render(request, 'profiles/promoter.html', context)

@login_required
def add_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            base_user = BaseUser.objects.get(user = request.user.id)
            promoter = Promoter.objects.get(base_user = base_user.id)
            newAlert = HelpAlert(
                                promoter=promoter,
                                name=form.cleaned_data['name'],
                                description=form.cleaned_data['description']
                                )
            newAlert.save()
            return HttpResponseRedirect('/profiles/')
        else:
            print("-------------------")
            print("Form is not valid")
            print(form.errors)
