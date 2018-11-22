"""
Created by: Django
Description: Functions for handling requests to the server
Modified by: Bernardo, Hugo, Alex, Francisco
Modify date: 02/11/2018
"""
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def get_promoter(user):
    base = BaseUser.objects.get(user=user)
    try:
        promoter = Promoter.objects.get(base_user=base)
    except Promoter.DoesNotExist:
        return False
    return promoter

# Create your views here.
@login_required
def index(request):
    if is_director(request.user):
        users = User.objects.all()
        accounts = []
        baseUsers = BaseUser.objects.filter(deleted_at__isnull=True)
        for baseUser in baseUsers:
            if is_promoter(baseUser.user):
                role = 'Promotora'
            else:
                role = baseUser.user.groups.all()[0]
            accounts.append({'account': baseUser,
                             'id': baseUser.id,
                             'name': baseUser.name,
                             'last_name_paternal': baseUser.last_name_paternal,
                             'last_name_maternal': baseUser.last_name_maternal,
                             'role': role
                            })
        return render(request, 'profiles/index.html', {'accounts': accounts})
    else:
        return HttpResponseRedirect('/administrative/')

@login_required
def delete_account(request, pk):
    print("Holaaa")
    if(is_director(request.user)):
        if request.method == 'GET':
            try:
                baseUser = BaseUser.objects.get(pk=pk)
            except BaseUser.DoesNotExist:
                raise Http404("No existe ese contacto.")

            baseUser.deleted_at = timezone.now()
            baseUser.user.is_active = False
            baseUser.user.save()
            baseUser.save()
            return HttpResponseRedirect('/profiles/')
        else:
            return HttpResponseRedirect('/profiles/')
    else:
        return HttpResponseRedirect('/profiles/')

@login_required
def users(request):
    """ Description: Renders the view of the accounts
        Parameters: request
        return: render
    """
    if(is_director(request.user)):
        all_users = BaseUser.objects.filter(deleted_at__isnull=True)
        all_promoters = Promoter.objects.all()
        promoters = []
        for promoter in all_promoters:
            promoters.append(BaseUser.objects.get(id = promoter.base_user_id))

        users = [user for user in all_users if user not in promoters]

        context = {'users': users}
        return render(request, 'profiles/users.html', context)
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
                print(newAlert.id)
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
                if User.objects.filter(username=username).exists():
                    messages.warning(request, 'El nombre de usuario ya existe, por favor ingresar otro')
                    form = BaseUserForm()
                    context = {'form': form}
                    return render(request, 'profiles/new_user.html', context)
                else:
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
def edit_user(request,pk):
    """ Description: Edits the information of an account
        Parameters: request, pk of the account that is edited
        return: render
    """
    if(is_director(request.user)):
        if request.method == 'POST':
            form = BaseUserForm(data=request.POST)

            if form.is_valid():
                base_user =  BaseUser.objects.get(id=pk)
                user_id = base_user.user_id

                user = User.objects.get(id=user_id)

                base_user.name=form.cleaned_data['name']
                base_user.last_name_paternal=form.cleaned_data['last_name_paternal']
                base_user.last_name_maternal=form.cleaned_data['last_name_maternal']
                base_user.phone_number=form.cleaned_data['phone_number']
                base_user.address=form.cleaned_data['address']
                base_user.email=form.cleaned_data['email']

                base_user.save()

                user.groups.clear()
                user.groups.add(form.cleaned_data['group'])

                return HttpResponseRedirect('/profiles/')
        else:
            base_user = BaseUser.objects.get(id=pk)
            user_id = base_user.user_id
            user = User.objects.get(id=user_id)
            form = BaseUserForm()
            group = ""
            for g in user.groups.all():
                group = g

            context = {'base_user': base_user, 'user': user, 'form': form, 'group': group}
            return render(request, 'profiles/edit_user.html', context)
    else:
        return HttpResponseRedirect('/profiles/')

@login_required
def get_promoter_profile(request,pk):
    if is_promoter(request.user):
        if request.method == 'GET':
            promoter = Promoter.objects.get(pk=pk)
            communities =  Community.objects.filter(deleted_at__isnull=True, promoter__id=pk)
            print(communities)
            context = {'promoter': promoter, 'communities': communities}
            return render(request, 'profiles/promoter_profile.html', context)
    else:
        return HttpResponseRedirect('/profiles/')

@login_required
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/administrative/')

@login_required
def edit_promoter(request, pk):
    """ Description: Edits the information of an account of a promoter
        Parameters: request, pk of the account that is edited
        return: render
    """
    if is_promoter(request.user):
        if request.method == 'POST':
            form = PromoterFormEdit(request.POST)
            if form.is_valid():
                promoter = get_object_or_404(Promoter, pk=pk)
                #Send the new clean data to the Tables
                #print(form.cleaned_data['communities'])
                if promoter.base_user.user.check_password(form.cleaned_data['previous_password']):
                    base_user = get_object_or_404(BaseUser, pk=promoter.base_user_id)
                    user = get_object_or_404(User, pk=base_user.user_id)

                    if form.cleaned_data['password'] != "" and form.cleaned_data['password'] != None:
                        user.password = form.cleaned_data['password']

                    #Data from base_user
                    if form.cleaned_data['name'] != "" and form.cleaned_data['name'] != None:
                        base_user.name=form.cleaned_data['name']
                    if form.cleaned_data['last_name_maternal'] != "" and form.cleaned_data['last_name_paternal'] != None:
                        base_user.last_name_maternal=form.cleaned_data['last_name_maternal']
                    if form.cleaned_data['last_name_paternal'] != "" and form.cleaned_data['last_name_paternal'] != None:
                        base_user.last_name_paternal=form.cleaned_data['last_name_paternal']
                    if form.cleaned_data['phone_number'] != "" and form.cleaned_data['phone_number'] != None:
                        base_user.phone_number=form.cleaned_data['phone_number']
                    if form.cleaned_data['address'] != "" and form.cleaned_data['address'] != None:
                        base_user.address=form.cleaned_data['address']
                    if form.cleaned_data['email'] != "" and form.cleaned_data['email'] != None:
                        base_user.email=form.cleaned_data['email']
                        #Data from promoter
                    if form.cleaned_data['contact_name'] != "" and form.cleaned_data['contact_name'] != None:
                        promoter.contact_name=form.cleaned_data['contact_name']
                    if form.cleaned_data['contact_phone_number'] != "" and form.cleaned_data['contact_phone_number'] != None:
                         promoter.contact_phone_number=form.cleaned_data['contact_phone_number']
                    promoter.communities.set(form.cleaned_data['communities'])

                    user.save()
                    base_user.save()
                    promoter.save()

                    messages.success(request, 'Datos guardados exitosamente')
                    return HttpResponseRedirect('/profiles/promoter_profile/%d/' %promoter.id)
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
                form = PromoterFormEdit()
                promoter = Promoter.objects.get(pk=pk)
                list = Community.objects.values_list('id', flat=True).filter(deleted_at__isnull=True, promoter__id=pk)
                communities = dict(zip(list[::1], list[::1]))
                context = {'form': form, 'promoter': promoter, 'communities':communities}
                return render(request, 'profiles/edit_promoter.html', context)

        elif request.method == 'GET':
            promoter = get_promoter(request.user)
            if promoter.id == pk:
                form = PromoterFormEdit()
                promoter = Promoter.objects.get(pk=pk)
                list = Community.objects.values_list('id', flat=True).filter(deleted_at__isnull=True, promoter__id=pk)
                communities = dict(zip(list[::1], list[::1]))
                context = {'form': form, 'promoter': promoter, 'communities':communities}
                return render(request, 'profiles/edit_promoter.html', context)
            else:
                return HttpResponseRedirect('/profiles/promoter_profile/'+str(pk))
        else:
            print("NOT POST OR GET")
    else:
        return HttpResponseRedirect('/administrative/')
