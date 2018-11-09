from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('new_alert/', views.add_alert, name='new_alert'),
    path('new_promoter/', views.add_promoter, name='new_promoter'),
    path('new_user/', views.add_user, name='new_user'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('promoter_profile/<int:pk>/', views.get_promoter_profile, name='promoter_profile'),
    path('logout/', views.logoutUser, name='logout')
]
