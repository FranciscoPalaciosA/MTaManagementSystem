from django.utils import timezone
from profiles.models import *

# Create your models here.
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

class ProductionReport(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    self_seed = models.IntegerField(default=0)
    self_leaf = models.IntegerField(default=0)
    self_flour = models.IntegerField(default=0)
    days_per_month = models.IntegerField(default=0)
    exch_seed = models.IntegerField(default=0)
    exch_leaf = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
