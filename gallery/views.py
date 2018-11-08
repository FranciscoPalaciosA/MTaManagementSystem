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
    form = PhotoForm()
    videoForm = VideoForm()
    context = {'form': form, 'videoForm': videoForm}
    return render(request, 'gallery/index.html', context)

@login_required
def new_photo(request):
    if not is_promoter(request.user):
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
            return HttpResponseRedirect('/gallery/')
    else:
        return HttpResponseRedirect('/gallery/')

@login_required
def new_video(request):
    if (is_administrative_assistant(request.user) | is_administrative_coordinator(request.user) | is_field_technician(request.user)):
        if request.method == 'POST':
            form = VideoForm(request.POST)
            if form.is_valid():
                video = Video(
                                title=form.cleaned_data['title'],
                                link=form.cleaned_data['link']
                            )
                video.save()
            return HttpResponseRedirect('/gallery/')
    else:
        return HttpResponseRedirect('/gallery/')
