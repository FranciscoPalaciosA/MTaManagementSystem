from django.db import models
from django.utils import timezone
from profiles.models import *

# Create your models here.
class ProductionReport(models.Model):
    self_seed = models.IntegerField(default=0)
    self_leaf = models.IntegerField(default=0)
    self_flour = models.IntegerField(default=0)
    days_per_month = models.IntegerField(default=0)
    exch_seed = models.IntegerField(default=0)
    exch_leaf = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

class Beneficiary(models.Model):
    name = models.CharField(max_length=50)
    last_name_paternal = models.CharField(max_length=50)
    last_name_maternal = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    community_name = models.CharField(max_length=50)
    num_of_family_beneficiaries = models.IntegerField(default=0)
    contact_name = models.CharField(max_length=200)
    contact_phone = models.IntegerField(default=0)
    account_number = models.IntegerField(default=0)
    bank_name = models.CharField(max_length=100)
    promoter = models.ManyToManyField(Promoter)
    #program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class WeeklySessionEvidence(models.Model):
    path = models.CharField(max_length=100)

class WeeklySession(models.Model):
    promoter = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    assistants = models.ManyToManyField(Beneficiary, verbose_name="list of assistants")
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)

    #evidences = models.ManyToManyField(WeeklySessionEvidence, verbose_name="evidences")

    def __str__(self):
        return str(self.type) + "-" +str(self.topic)
