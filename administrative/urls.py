from django.urls import path
from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('production_report/', views.production_report, name='production_report'),
    path('communities/', views.communities, name='communities'),
    path('beneficiaries/<int:pk>', views.beneficiaries, name='beneficiaries'),
    path('new_beneficiary/', views.add_beneficiary, name='new_beneficiary'),
    path('modify_beneficiary/', views.modify_beneficiary, name='modify_beneficiary'),
    path('production_report/', views.production_report, name='new_production_report'),
    path('production_report_list/', views.production_report_list, name='production_report_list'),
    path('administrative_production_report/<int:pk>', views.administrative_production_report, name='administrative_production_report'),
    path('weekly_sessions/', views.weekly_sessions, name='weekly_sessions'),
    path('get_weekly_session/<int:pk>/', views.get_weekly_session,  name='get_weekly_session'),
    path('new_saving_account/', views.add_saving_account, name='new_saving_account'),
    path('payments/', views.payments, name='payments'),
    path('get_payment/<int:pk>/', views.get_payment,  name='get_payment'),
    path('pay/<int:pk>/', views.payments, name='pay'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('alerts/', views.alert_list, name='alerts'),
    path('resolve_alert/<int:pk>/', views.resolve_alert, name='resolve_alert'),
    path('training_sessions/', views.training_session, name='training_session'),
    path('ajax/load_communities/', views.load_communities, name='ajax_load_communities')
]
