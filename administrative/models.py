from django.db import models
from django.utils import timezone
from django.dispatch import receiver
import os

# from profiles.models import *

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
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    num_of_family_beneficiaries = models.IntegerField(default=0)
    contact_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=50, default=0)
    account_number = models.CharField(max_length=50, default=0)
    bank_name = models.CharField(max_length=100)
    promoter = models.ForeignKey('profiles.Promoter', on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    member_in = models.ManyToManyField(Program, through='BeneficiaryInProgram')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class BeneficiaryInProgram(models.Model):
    status_choices = (('Otro', 'Otro'), ('Concluída', 'Concluída'), ('En uso', 'En uso'), ('En obra', 'En obra'))
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
    self_seed = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    self_leaf = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    self_flour = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    days_per_month = models.IntegerField(default=0)
    exch_seed = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    exch_leaf = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    want_for_seed = models.CharField(max_length=100, null=True)
    want_for_leaf = models.CharField(max_length=100, null=True)
    get_for_seed_qty = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    get_for_leaf_qty = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Production Report " + str(self.id)

class WeeklySession(models.Model):
    promoter = models.ForeignKey('profiles.Promoter', on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    assistants = models.ManyToManyField(Beneficiary, verbose_name="list of assistants")
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)

    def __str__(self):
        return str(self.type) + "-" +str(self.topic)

class SavingAccount(models.Model):
    name = models.CharField(max_length=50)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    municipality = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    list_of_beneficiaries =models.ManyToManyField(Beneficiary, verbose_name="list of beneficiaries")
    total_saved_amount = models.IntegerField(default=0)
    president_beneficiary = models.ForeignKey(Beneficiary,related_name='president', on_delete=models.CASCADE)
    treasurer_beneficiary = models.ForeignKey(Beneficiary, related_name='treasurer',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + "-" +str(self.community)

class SavingsLog(models.Model):
    saving_account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return str(self.saving_account) + " : " + str(self.month) + "/" + str(self.year)

class WeeklySessionEvidence(models.Model):
    weekly_session = models.ForeignKey(WeeklySession, on_delete=models.CASCADE)
    evidence = models.ImageField(upload_to = 'administrative/static/weekly_session_evidence/', default = 'administrative/weekly_session_evidence/no-img.jpg')

    def __str__(self):
        return str(self.weekly_session) + " Ev: " + str(self.evidence)

    def image_url(self):
        return str(self.evidence).split('administrative/')[-1]

@receiver(models.signals.post_delete, sender=WeeklySessionEvidence)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `WeeklySessionEvidence` object is deleted.
    """
    if instance.evidence:
        if os.path.isfile(instance.evidence.path):
            os.remove(instance.evidence.path)

class Payment(models.Model):
    promoter = models.ForeignKey('profiles.Promoter', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    due_date = models.DateTimeField()
    pay_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(blank=True, max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.description)

class TrainingSession(models.Model):
    topic_choices = (
                        ('Health', 'Salud'),
                        ('Cook', 'Cocina Con Amaranto'),
                        ('MV', 'Mística y Valores'),
                        ('Work', 'Competencias Laborales'),
                        ('Motivation', 'Motivación y Desarrollo Humano'),
                        ('Entrepeneur', 'Emprendedurismo'),
                        ('Other', 'Otro')
                    )
    trainer = models.ForeignKey('profiles.BaseUser', on_delete=models.CASCADE)
    assistants = models.ManyToManyField(Beneficiary, verbose_name='list of beneficiaries')
    date = models.DateField()
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    topic = models.CharField(max_length=250, choices=topic_choices, default='Otro')
    comments = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.topic + " - " + str(self.date)

class TrainingSessionEvidence(models.Model):
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    evidence = models.ImageField(upload_to = 'administrative/static/training_session_evidence/', default = 'administrative/training_session_evidence/no-img.jpg')

    def __str__(self):
        return str(self.training_session) + " Ev: " + str(self.evidence)

    def image_url(self):
        return str(self.evidence).split('administrative/')[-1]
