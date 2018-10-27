from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class BaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name_paternal = models.CharField(max_length=50)
    last_name_maternal = models.CharField(max_length=50)
    #profile_picture = models.ImageField(upload_to='images/profiles/%Y/%m/%d', blank=True)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    position = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user.username

class Promoter(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    #community = models.ForeignKey('administrative.Community', on_delete=models.CASCADE)
    communities = models.ManyToManyField('administrative.Community')
    contact_name = models.CharField(max_length=50)
    contact_phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.base_user.name + " " + self.base_user.last_name_paternal


class HelpAlert(models.Model):
    promoter = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.promoter.base_user.name + " " + self.promoter.base_user.last_name_paternal + " - " + self.name
