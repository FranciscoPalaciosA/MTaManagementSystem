from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_alert/', views.add_alert, name='new_alert'),
    path('new_promoter/', views.add_promoter, name='new_promoter'),
    path('new_user/', views.add_user, name='new_user'),
    path('i18n/', include('django.conf.urls.i18n')),
]
