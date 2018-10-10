from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *


# Create your views here.
@login_required
def index(request):
    return HttpResponse("Directory Index")

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
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            newContact = Contact(
                                first_name = forms.cleaned_data['first_name'],
                                last_name_paternal = forms.cleaned_data['last_name_paternal'],
                                last_name_maternal = forms.cleaned_data['last_name_maternal'],
                                phone_number = forms.cleaned_data['phone_number'],
                                email = forms.cleaned_data['email'],
                                contact_type = forms.cleaned_data['contact_type'],
                                comments = forms.cleaned_data['comments']
                                )
            newContact.save()
            return HttpResponseRedirect('/directory/')

    else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")
