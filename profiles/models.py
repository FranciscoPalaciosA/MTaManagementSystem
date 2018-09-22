from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class BaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name_paternal = models.CharField(max_length=50)
    last_name_maternal = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='images/profiles/%Y/%m/%d', blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)


class Promoter(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    
