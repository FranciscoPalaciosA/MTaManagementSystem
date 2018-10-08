from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProductionReport)
admin.site.register(Beneficiary)
admin.site.register(Program)
admin.site.register(BeneficiaryInProgram)
admin.site.register(WeeklySession)
