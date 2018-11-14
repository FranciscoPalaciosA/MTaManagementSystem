"""
Created by: Django
Description: Functions for handling requests to the server
Modified by: Bernardo, Hugo, Alex, Francisco
Modify date: 07/11/2018
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
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
    contact_list = {
        'admin': Contact.objects.filter(deleted_at__isnull=True, contact_type='Admin'),
        'volunteer': Contact.objects.filter(deleted_at__isnull=True, contact_type='Volunteer'),
        'volunteer': Contact.objects.filter(deleted_at__isnull=True, contact_type='Volunteer'),
        'ext_cons': Contact.objects.filter(deleted_at__isnull=True, contact_type='Ext_Cons'),
        'simp': Contact.objects.filter(deleted_at__isnull=True, contact_type='Simp'),
        'other': Contact.objects.filter(deleted_at__isnull=True, contact_type='Other'),
    }

    isDirector = is_director(request.user)
    context = {
        'type_list': Contact.type_choices,
        'contact_list': contact_list,
        'director': isDirector
    }

    return render(request, 'directory/index.html', context)

@login_required
def contact(request):
    form = ContactForm()
    context = {'form': form}
    return render(request, 'directory/new_contact.html', context)
# Function that renders the form to add a new contact_type
# Input: a GET or POST request
# Output: a rendered form if it is a GET request, and a redirection to /directory/ if it is a POST request
@login_required
def add_contact(request):
    contact_list = Contact.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            newContact = Contact(
                                first_name = form.cleaned_data['first_name'],
                                last_name_paternal = form.cleaned_data['last_name_paternal'],
                                last_name_maternal = form.cleaned_data['last_name_maternal'],
                                phone_number = form.cleaned_data['phone_number'],
                                email = form.cleaned_data['email'],
                                contact_type = form.cleaned_data['contact_type'],
                                institution = form.cleaned_data['institution'],
                                comments = form.cleaned_data['comments'],
                                )
            newContact.save()
            return HttpResponseRedirect('/directory/')

        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")

    elif request.method == 'GET':
        form = ContactForm()
        context = {'form': form}
        return render(request, 'directory/new_contact.html', context)

@login_required
def delete_contact(request, pk):
    if(is_director(request.user)):
        if request.method == 'GET':
            try:
                contact = Contact.objects.get(pk=pk)
            except Contact.DoesNotExist:
                raise Http404("No existe ese contacto.")

            contact.deleted_at = timezone.now()
            contact.save()
        else:
            return HttpResponseRedirect('/directory/')
    else:
        return HttpResponseRedirect('/directory/')


def edit_contact(request,pk):
    """ Description: Edits the information of a contact
        Parameters: request, pk of the contact that is edited
        return: render
    """
    if not (is_promoter(request.user)):
        if request.method == 'POST':
            form = ContactForm(data=request.POST)

            if form.is_valid():
                contact =  Contact.objects.get(id=pk)

                contact.first_name = form.cleaned_data['first_name']
                contact.last_name_paternal = form.cleaned_data['last_name_paternal']
                contact.last_name_maternal = form.cleaned_data['last_name_maternal']
                contact.phone_number = form.cleaned_data['phone_number']
                contact.email = form.cleaned_data['email']
                contact.contact_type = form.cleaned_data['contact_type']
                contact.institution = form.cleaned_data['institution']
                contact.comments = form.cleaned_data['comments']

                contact.save()

                return HttpResponseRedirect('/directory/')
        else:
            contact = Contact.objects.get(id=pk)
            form = ContactForm()
            context = {'contact': contact, 'form': form}
            return render(request, 'directory/edit_contact.html', context)
    else:
        return HttpResponseRedirect('/directory/')

@login_required
def add_institution(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid():
            newInstitution = Institution(
                                name = form.cleaned_data['name'],
                                type_of_institution = form.cleaned_data['type_of_institution'],
                                comments = form.cleaned_data['comments'],
                                )
            newInstitution.save()
            return HttpResponseRedirect('/directory/')

        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")

    elif request.method == 'GET':
        form = InstitutionForm()
        context = {'form': form}
        return render(request, 'directory/new_institution.html', context)

@login_required
def institution_directory(request):
    institution_list = {
        'foundations': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Foundations'),
        'enterprise': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Enterprise'),
        'local_gob': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Local_Gob'),
        'fed_gob': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Fed_Gob'),
        'education': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Education'),
        'scientific': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Scientific'),
        'other': Institution.objects.filter(deleted_at__isnull=True, type_of_institution='Other'),
    }
    context = {
        'type_list': Institution.institution_choices,
        'institution_list': institution_list
    }
    return render(request, 'directory/list_of_institutions.html', context)
