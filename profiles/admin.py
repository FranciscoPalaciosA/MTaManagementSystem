from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Promoter)
admin.site.register(HelpAlert)
admin.site.register(AdminUser)
