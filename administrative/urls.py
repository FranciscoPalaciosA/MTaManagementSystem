from django.urls import path

from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('production_report/', views.fill_Production_Report, name='production_report'),
    path('weekly_sessions/', views.weekly_sessions, name='weekly_sessions'),
]
