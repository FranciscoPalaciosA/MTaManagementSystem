from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Community)
admin.site.register(ProductionReport)
admin.site.register(Beneficiary)
admin.site.register(Program)
admin.site.register(BeneficiaryInProgram)
admin.site.register(WeeklySession)
admin.site.register(WeeklySessionEvidence)
admin.site.register(Payment)
admin.site.register(SavingAccount)
admin.site.register(SavingsLog)
admin.site.register(TrainingSession)
admin.site.register(TrainingSessionEvidence)
