from django.urls import path
from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('communities/', views.communities, name='communities'),
    path('beneficiaries/', views.beneficiaries_list, name='beneficiaries_list'),
    path('beneficiaries/<int:pk>', views.beneficiaries, name='beneficiary'),
    path('new_beneficiary/', views.add_beneficiary, name='new_beneficiary'),
    path('edit_beneficiary/<int:pk>/', views.edit_beneficiary, name='edit_beneficiary'),
    path('modify_beneficiary/', views.modify_beneficiary, name='modify_beneficiary'),
    path('remove_from_program/<int:p_id>/', views.remove_from_program, name='remove_from_program'),
    path('production_report/', views.production_report, name='production_report'),
    path('production_report_list/', views.production_report_list, name='production_report_list'),
    path('administrative_production_report/<int:pk>', views.administrative_production_report, name='administrative_production_report'),
    # Promoter Stuff
    path('weekly_sessions/', views.weekly_sessions, name='weekly_sessions'),
    path('edit_weekly_session/<int:pk>/', views.edit_weekly_session, name='edit_weekly_session'),
    path('get_weekly_session/<int:pk>/', views.get_weekly_session,  name='get_weekly_session'),
    path('payments/', views.payments, name='payments'),
    path('get_payment/<int:pk>/', views.get_payment,  name='get_payment'),
    path('pay/<int:pk>/', views.payments, name='pay'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('alerts/', views.alert_list, name='alerts'),
    path('resolve_alert/<int:pk>/', views.resolve_alert, name='resolve_alert'),
    path('my_communities/', views.my_communities, name='my_communities'),
    # Savings
    path('saving_accounts/', views.saving_accounts, name='saving_accounts'),
    path('new_saving_account/', views.add_saving_account, name='new_saving_account'),
    path('edit_savings/<int:pk>/', views.edit_savings, name='edit_savings'),
    path('edit_savings/', views.edit_savings, name='edit_savings'),
    # Other
    path('training_sessions/', views.training_session, name='training_session'),
    path('ajax/load_communities/', views.load_communities, name='ajax_load_communities'),
    path('reports/', views.community_report, name='community_report'),
    path('reports/municipality_savings/', views.get_communities_savings, name='ajax_savings'),
    path('reports/municipality_beneficiaries/', views.get_communities_beneficiaries, name='ajax_ben_mun'),
    path('reports/program_beneficiaries/', views.get_program_beneficiaries, name='ajax_ben_prog'),
]
