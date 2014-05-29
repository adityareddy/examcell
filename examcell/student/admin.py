from django.contrib import admin

# Register your models here.
from student.models import Applications, Student

admin.site.register(Applications)
admin.site.register(Student)