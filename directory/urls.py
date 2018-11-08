from django.urls import path

from . import views

app_name = 'directory'
urlpatterns = [
    path ('', views.index, name='index'),
    path ('register_contact/', views.contact, name='register_contact'),
    path ('new_contact/', views.add_contact, name='new_contact'),
    path ('new_institution/', views.add_institution, name='new_institution'),
    path ('institution_directory/', views.institution_directory, name='institution_directory'),
    path ('delete_contact/<int:pk>', views.delete_contact, name='delete_contact')
]
