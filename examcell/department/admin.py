from django.contrib import admin

# Register your models here.
from department.models import Department, Subject#, Detained, Condonation


admin.site.register(Department)
admin.site.register(Subject)
# admin.site.register(Detained)
# admin.site.register(Condonation)