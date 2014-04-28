from django.contrib.auth.models import User
from django.db import models
from student.models import Student

class Department(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=128)

class Subject(models.Model):
    code = models.CharField(max_length=32)
    department = models.ForeignKey(Department)
    semester = models.IntegerField()
    title = models.CharField(max_length=256)
    theoryOrLab = models.CharField(max_length=1)
    optional = models.BooleanField()

class Detained(models.Model):
    department = models.ForeignKey(Department)
    students = models.ManyToManyField(Student)

class Condonation(models.Model):
    department = models.ForeignKey(Department)
    students = models.ManyToManyField(Student)
    amount = models.FloatField()
