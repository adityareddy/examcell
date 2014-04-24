from django.db import models

class Student(models.Model):
	reg_id=models.CharField(max_length=15)
	first_name=models.CharField(max_length=128)
	last_name=models.CharField(max_length=128)
	email=models.EmailField()
	phno=models.IntegerField()
	gender=models.CharField(max_length=2)
	city=models.CharField(max_length=128)
	state=models.CharField(max_length=128)
	pincode=models.IntegerField()
	branch=models.CharField(max_length=128)
	year=models.IntegerField()
	sem=models.IntegerField()
	photo=models.ImageField(upload_to='/static/')
	sign=models.ImageField(upload_to='/static/')

