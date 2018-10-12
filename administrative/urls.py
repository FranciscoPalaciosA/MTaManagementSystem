from django.urls import path
from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('production_report/', views.production_report, name='production_report'),
    path('beneficiaries/', views.beneficiaries, name='beneficiaries'),
    path('new_beneficiary/', views.add_beneficiary, name='new_beneficiary'),
    path('new_production_report/', views.add_production_report, name='new_production_report'),
    path('weekly_sessions/', views.weekly_sessions, name='weekly_sessions'),
    path('new_saving_account/', views.saving_account, name='new_saving_account'),
]
