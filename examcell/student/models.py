from django.db import models
from django.contrib.auth.models import User
from home.models import Notification

class Student(models.Model):
	user=models.OneToOneField(User)
	reg_id=models.CharField(max_length=15)
	first_name=models.CharField(max_length=128)
	last_name=models.CharField(max_length=128)
	email=models.EmailField()
	phone_number=models.IntegerField()
	gender=models.CharField(max_length=2)
	state=models.CharField(max_length=128)
	city=models.CharField(max_length=128)
	pincode=models.IntegerField()
	branch=models.CharField(max_length=128)
	semester=models.IntegerField()
	photo=models.ImageField(upload_to='static/student_photos')
	sign=models.ImageField(upload_to='static/student_signatures')

class Applications(models.Model):
	student = models.ForeignKey(Student)
	notification = models.ForeignKey(Notification)
	verified = models.BooleanField()