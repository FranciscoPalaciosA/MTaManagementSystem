"""
Created by: Django
Description: Register models to manage in the admin site
Modified by: Bernardo
Modify date: 22/10/2018
"""
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Photo)
