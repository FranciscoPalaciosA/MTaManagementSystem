"""
Created by: Django
Description: Functions for handling requests to the server
Modified by: Bernardo, Hugo, Alex, Francisco
Modify date: 02/11/2018
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from .models import *
from .forms import *

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
    if user:
        return user.groups.filter(name='Director').count() == 1
    return False

def is_trainer(user):
    if user:
        return user.groups.filter(name='Capacitador').count() == 1
    return False

def is_administrative_assistant(user):
    if user:
        return user.groups.filter(name='Asistente Administrativo').count() == 1
    return False

def is_administrative_coordinator(user):
    if user:
        return user.groups.filter(name='Coordinador Administrativo').count() == 1
    return False

def is_field_technician(user):
    if user:
        return user.groups.filter(name='Técnico de Campo').count() == 1
    return False

# Create your views here.
@login_required
def index(request):
    alert_form = AlertForm()
    context = {'alert_form': alert_form}
    return render(request, 'profiles/promoter.html', context)

@login_required
def accounts(request):
    """ Description: Renders the view of the accounts
        Parameters: request
        return: render
    """
    if(is_director(request.user)):
        users = BaseUser.objects.filter(deleted_at__isnull=True)
        context = {'users': users}
        return render(request, 'profiles/accounts.html', context)
    else:
        return HttpResponseRedirect('/profiles/')

@login_required
def edit_account(request,pk):
    if(is_director(request.user)):
        if request.method == 'POST':
            form = BaseUserForm(request.POST)

            if form.is_valid():
                user =  BaseUser.objects.get(id=pk)

                user.name=form.cleaned_data['name']
                user.last_name_paternal=form.cleaned_data['last_name_paternal']
                user.last_name_maternal=form.cleaned_data['last_name_maternal']
                user.phone_number=form.cleaned_data['phone_number']
                user.address=form.cleaned_data['address']
                user.email=form.cleaned_data['email']

                user.save()
                
                return HttpResponseRedirect('/profiles/accounts/')
        else:
            user = BaseUser.objects.get(id=pk)
            form = BaseUserForm()
            context = {'user': user, 'form': form}
            return render(request, 'profiles/edit_account.html', context)
    else:
        return HttpResponseRedirect('/profiles/')

@login_required
def add_alert(request):
    if is_promoter(request.user):
        if request.method == 'POST':
            form = AlertForm(request.POST)
            if form.is_valid():
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
        return HttpResponseRedirect('/profiles/')

@login_required
def add_promoter(request):
    if not is_promoter(request.user):
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
                                        #,communities=form.cleaned_data['communities']
                                    )
                promoter.save()
                promoter.communities.set(form.cleaned_data['communities'])
                return HttpResponseRedirect('/profiles/')
        elif request.method == 'GET':
            form = PromoterForm()
            context = {'form': form}
            return render(request, 'profiles/new_promoter.html', context)
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def add_user(request):
    if not is_promoter(request.user):
        if request.method == 'POST':
            form = BaseUserForm(request.POST)
            if form.is_valid():
                #Create the Django User (The one that accesses the system)
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user.groups.add(form.cleaned_data['group'])
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
                return HttpResponseRedirect('/profiles/')
        elif request.method == 'GET':
            form = BaseUserForm()
            context = {'form': form}
            return render(request, 'profiles/new_user.html', context)
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def get_promoter_profile(request,pk):
    if request.method == 'GET':
        promoter = Promoter.objects.get(pk=pk)
        communities =  Community.objects.filter(deleted_at__isnull=True, promoter__id=pk)
        print(communities)
        context = {'promoter': promoter, 'communities': communities}
        return render(request, 'profiles/promoter_profile.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/administrative/')
