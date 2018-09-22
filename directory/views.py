from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *


# Create your views here.
@login_required
def index(request):
    contact_list = Contact.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            newContact = Contact(
                                first_name=form.cleaned_data['first_name'],
                                last_name=form.cleaned_data['last_name'],
                                phone_number=form.cleaned_data['phone_number'],
                                institution=form.cleaned_data['institution'])
            newContact.save()
            return HttpResponseRedirect('/directory/')
    else:
        form = ContactForm()
        context = {'contacts': contact_list, 'form': form}
    return render(request, 'directory/index.html', context)
