"""
Created by: Django
Description: Functions for handling requests to the server
Modified by: Bernardo, Hugo, Alex, Francisco
Modify date: 22/10/2018
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib import messages
from django.utils import timezone

from profiles.models import HelpAlert
from django.http import Http404
from .models import *
from .forms import *
from datetime import datetime, time

# Create your views here.
def index(request):
    form = PhotoForm()
    context = {'form': form}
    return render(request, 'gallery/index.html', context)

@login_required
def new_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            # print(images)
            photo = Photo(
                            title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            image=form.cleaned_data['image']
                        )
            photo.save()
            print("SUCCESS!!")
        else:
            print('----------')
            print(form.errors)
            # for e in form.errors:
            #     print(e)
            print('----------')
        context = {'form': form}
        return render(request, 'gallery/index.html', context)
