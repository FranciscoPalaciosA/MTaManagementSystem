from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from .forms import *


# Create your views here.
@login_required
def index(request):
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

@login_required
def add_promoter(request):
    if request.method == 'POST':
        form = PromoterForm(request.POST)
        if form.is_valid():
            #Create the Django User (The one that accesses the system)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            #Create the BaseUser object
            base_user = BaseUser(
                                    user=user,
                                    name=form.cleaned_data['name'],
                                    last_name_maternal=form.cleaned_data['last_name_maternal'],
                                    last_name_paternal=form.cleaned_data['last_name_paternal'],
                                    phone_number=form.cleaned_data['phone_number'],
                                    address=form.cleaned_data['address'],
                                    email=form.cleaned_data['email']
                                )
            base_user.save()
            #Create the Promoter object
            promoter = Promoter(
                                    base_user=base_user,
                                    contact_name=form.cleaned_data['contact_name'],
                                    contact_phone_number=form.cleaned_data['contact_phone_number']
                                )
            promoter.save()
            return HttpResponseRedirect('/profiles/')
        else:
            print('----Invalid form-----')
            print(form.errors)
    elif request.method == 'GET':
        form = PromoterForm()
        context = {'form': form}
        return render(request, 'profiles/new_promoter.html', context)
