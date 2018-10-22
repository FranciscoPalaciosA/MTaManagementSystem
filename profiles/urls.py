from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_alert/', views.add_alert, name='new_alert'),
    path('new_promoter/', views.add_promoter, name='new_promoter'),
    path('new_user/', views.add_user, name='new_user'),
    path('edit_promoter/<int:pk>/', views.edit_promoter, name='edit_promoter'),
]
