from django.contrib import admin
from .models import ProductionReport
from .models import Beneficiary

# Register your models here.
admin.site.register(ProductionReport)
admin.site.register(Beneficiary)
