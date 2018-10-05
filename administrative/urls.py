from django.urls import path

from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('production_report/', views.fill_Production_Report, name='production_report'),
    path('beneficiaries/', views.beneficiaries, name='beneficiaries'),
    path('new_beneficiary/', views.add_beneficiary, name='new_beneficiary'),
]
