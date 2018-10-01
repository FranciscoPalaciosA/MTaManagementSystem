from django.db import models
from django.utils import timezone

# Create your models here.
class ProductionReport(models.Model):
    self_seed = models.IntegerField(default=0)
    self_leaf = models.IntegerField(default=0)
    self_flour = models.IntegerField(default=0)
    days_per_montt = models.IntegerField(default=0)
    exch_seed = models.IntegerField(default=0)
    exch_leaf = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
