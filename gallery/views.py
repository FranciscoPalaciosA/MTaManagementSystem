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

from urllib.parse import urlparse
from urllib.parse import parse_qs

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

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

# Create your views here.
@login_required
def index(request):
    if not is_promoter(request.user):
        form = PhotoForm()
        videoForm = VideoForm()
        photos = Photo.objects.all()
        videos = Video.objects.all()
        objVideos = []
        for video in videos:
            id = video_id(video.link)
            objVideos.append({
                                'title': video.title,
                                'link': video.link,
                                'id': id
                            })

        context = {'form': form, 'videoForm': videoForm, 'photos': photos, 'videos': objVideos}
        return render(request, 'gallery/index.html', context)
    return HttpResponseRedirect('/administrative/')

@login_required
def new_photo(request):
    if (is_administrative_assistant(request.user) | is_administrative_coordinator(request.user) | is_field_technician(request.user)):
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                # print(images)
                ext = str(form.cleaned_data['image'])
                ext = ext.split(".")
                ext = ext[-1].lower()
                if ext in ['.png', 'jpg', '.jpeg', '.gif', 'tif']:
                    photo = Photo(
                                    title=form.cleaned_data['title'],
                                    description=form.cleaned_data['description'],
                                    image=form.cleaned_data['image']
                                )
                    photo.save()
                else:
                    print('--------')
                    print("not an image file")
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
