from django.db import models
from django.contrib.auth.models import User
from home.models import Notification

SEMESTER_CHOICES = (
(1,'I'),
(2,'II'),
(3,'III'),
(4,'IV'),
(5,'V'),
(6,'VI'),
(7,'VII'),
(8,'VIII')
)

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
	semester=models.IntegerField(choices=SEMESTER_CHOICES)
	photo=models.ImageField(upload_to='static/student_photos')
	sign=models.ImageField(upload_to='static/student_signatures')

class Applications(models.Model):
	student = models.ForeignKey(Student)
	notification = models.ForeignKey(Notification)
	amount =  models.IntegerField()
	verified = models.BooleanField()
	paid = models.BooleanField()