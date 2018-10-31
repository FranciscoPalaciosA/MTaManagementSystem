from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *


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
    print("-----------------------------------------------")
    print(contact_list)
    print("-----------------------------------------------")
    context = {
        'type_list': Contact.type_choices,
        'contact_list': contact_list
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
