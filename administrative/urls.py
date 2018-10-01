from django.urls import path

from . import views

app_name = 'administrative'
urlpatterns = [
    path('', views.index, name='index'),
    path('fill_Production_Report/', views.fill_Production_Report, name='fill_Production_Report'),
]
