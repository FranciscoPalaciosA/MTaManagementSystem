from django.urls import path
from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('production_report/', views.production_report, name='production_report'),
    path('communities/', views.communities, name='communities'),
    path('beneficiaries/', views.beneficiaries, name='beneficiaries'),
    path('new_beneficiary/', views.add_beneficiary, name='new_beneficiary'),
    path('production_report/', views.add_production_report, name='production_report'),
    path('new_production_report/', views.production_report, name='new_production_report'),
    path('production_report_list/', views.production_report_list, name='production_report_list'),
    path('weekly_sessions/', views.weekly_sessions, name='weekly_sessions'),
    path('payments/', views.payments, name='payments'),
    path('pay/<int:pk>/', views.pay, name='pay'),
    path('alerts/', views.alert_list, name='alerts'),
    path('resolve_alert/<int:pk>/', views.resolve_alert, name='resolve_alert'),
]
