"""
Created by: Django
Description: Define url paths for accessing different views
Modified by: Bernardo, Hugo
Modify date: 31/10/2018
"""

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gallery'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_photo/', views.new_photo, name='new_photo'),
    path('new_video/', views.new_video, name='new_video'),
]
