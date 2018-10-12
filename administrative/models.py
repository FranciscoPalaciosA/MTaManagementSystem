from django.db import models
from django.utils import timezone
from profiles.models import *

# Create your models here.

class Program(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)
        
class Community(models.Model):
    name = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

    def __str__(self):
        return str(self.name)

class Beneficiary(models.Model):
    name = models.CharField(max_length=50)
    last_name_paternal = models.CharField(max_length=50)
    last_name_maternal = models.CharField(max_length=50)
    num_of_family_beneficiaries = models.IntegerField(default=0)
    contact_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=50, default=0)
    account_number = models.IntegerField(default=0)
    bank_name = models.CharField(max_length=100)
    promoter = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    member_in = models.ManyToManyField(Program, through='BeneficiaryInProgram')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class BeneficiaryInProgram(models.Model):
    status_choices = (('Other', 'Otro'), ('Done', 'Concluída'), ('In use', 'En uso'), ('Not done', 'En obra'))
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    curp = models.CharField(max_length=50)
    house_address = models.CharField(max_length=100)
    house_references = models.CharField(max_length=120)
    huerto_coordinates = models.CharField(max_length=100)
    water_capacity = models.IntegerField(default=0)
    cisterna_location = models.CharField(max_length=120)
    cisterna_status = models.CharField(max_length=120, choices=status_choices, default='Otro')
    school = models.CharField(max_length=120)
    age = models.IntegerField(default=0)
    initial_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    savings_account_role = models.CharField(max_length=50)

    def __str__(self):
        return str(self.beneficiary.name) + " - " + str(self.program.name)


class ProductionReport(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    self_seed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    self_leaf = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    self_flour = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    days_per_month = models.IntegerField(default=0)
    exch_seed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    want_for_seed = models.CharField(max_length=100)
    want_for_seed_qty = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exch_leaf = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    want_for_leaf = models.CharField(max_length=100)
    want_for_leaf_qty = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Production Report " + str(self.id)

class WeeklySession(models.Model):
    promoter = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    assistants = models.ManyToManyField(Beneficiary, verbose_name="list of assistants")
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.type) + "-" +str(self.topic)

class WeeklySessionEvidence(models.Model):
    weekly_session = models.ForeignKey(WeeklySession, on_delete=models.CASCADE)
    evidence = models.ImageField(upload_to = 'administrative/weekly_session_evidence/', default = 'administrative/weekly_session_evidence/no-img.jpg')

    def __str__(self):
        return str(self.weekly_session) + " Ev: " + str(self.evidence)
