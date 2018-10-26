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
