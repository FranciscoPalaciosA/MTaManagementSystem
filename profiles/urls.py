from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_alert/', views.add_alert, name='new_alert'),
]
