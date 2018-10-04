from django.urls import path
from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('production_report/', views.production_report, name='production_report'),
    path('new_production_report/', views.add_production_report, name='new_production_report'),
]
