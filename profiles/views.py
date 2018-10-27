from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
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
                                    #,communities=form.cleaned_data['communities']
                                )
            promoter.save()
            promoter.communities.set(form.cleaned_data['communities'])
            return HttpResponseRedirect('/profiles/')
    elif request.method == 'GET':
        form = PromoterForm()
        context = {'form': form}
        return render(request, 'profiles/new_promoter.html', context)


@login_required
def add_user(request):
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

@login_required
def edit_promoter(request, pk):
    if request.method == 'POST':
        form = PromoterFormEdit(request.POST)
        if form.is_valid():
            promoter = get_object_or_404(Promoter, pk=pk)
            #Send the new clean data to the Tables
            print(form.cleaned_data['communities'])
            if promoter.base_user.user.check_password(form.cleaned_data['previous_password']):
                if form.cleaned_data['password'] != "" and form.cleaned_data['password'] != None:
                    promoter.base_user.user.password = form.cleaned_data['password'],
                #Data from base_user
                if form.cleaned_data['name'] != "" and form.cleaned_data['name'] != None:
                    promoter.base_user.name=form.cleaned_data['name'],
                if form.cleaned_data['last_name_maternal'] != "" and form.cleaned_data['last_name_paternal'] != None:
                    promoter.base_user.last_name_maternal=form.cleaned_data['last_name_maternal'],
                if form.cleaned_data['last_name_paternal'] != "" and form.cleaned_data['last_name_paternal'] != None:
                    promoter.base_user.last_name_paternal=form.cleaned_data['last_name_paternal'],
                if form.cleaned_data['phone_number'] != "" and form.cleaned_data['phone_number'] != None:
                    promoter.base_user.phone_number=form.cleaned_data['phone_number'],
                if form.cleaned_data['adress'] != "" and form.cleaned_data['adress'] != None:
                    promoter.base_user.address=form.cleaned_data['address'],
                if form.cleaned_data['email'] != "" and form.cleaned_data['email'] != None:
                    promoter.base_user.email=form.cleaned_data['email'],
                    #Data from promoter
                if form.cleaned_data['contact_name'] != "" and form.cleaned_data['contact_name'] != None:
                    promoter.contact_name=form.cleaned_data['contact_name'],
                if form.cleaned_data['contact_phone_number'] != "" and form.cleaned_data['contact_phone_number'] != None:
                    promoter.contact_phone_number=form.cleaned_data['contact_phone_number'],
                promoter.communities.set(form.cleaned_data['communities'])
                promoter.save()
                messages.success(request, 'Datos guardados exitosamente')
                return HttpResponseRedirect('/profiles/')
            else:
                form = PromoterFormEdit()
                context = {'form': form, 'promoter': promoter}
                messages.warning(request, 'La contraseña anterior es incorrecta')
                return render(request, 'profiles/edit_promoter.html', context)
        else:
            print("Invalid form")
            messages.warning(request, 'No ha llenado todos los espacios de la forma')
            for error in form.errors:
                print(error)
    elif request.method == 'GET':
        form = PromoterFormEdit()
        promoter = Promoter.objects.get(pk=pk)
        context = {'form': form, 'promoter': promoter}
        return render(request, 'profiles/edit_promoter.html', context)
    else:
        print("NOT POST OR GET")
