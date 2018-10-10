from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    type_choices = (('Admin', 'Administrativo'), ('Volunteer','Voluntario'),('Ext_Cons','Consultor Externo'),('Simp','Simpatizante'),('Other', 'Otro'))

    first_name = models.CharField(max_length=50)
    last_name_paternal = models.CharField(max_length=50)
    last_name_maternal = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    contact_type = models.CharField(max_length=100, choices=type_choices, default='Otro')
    comments = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default = True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class ContactTypeInfo(models.Model):
    institution = models.CharField(max_length=50)
