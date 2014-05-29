from django.db import models

class Notification(models.Model):
    type = models.CharField(max_length=6)
    dept = models.CharField(max_length=16)
    sem = models.IntegerField()
    amount = models.FloatField()
    fine = models.FloatField()
    lastdate = models.DateField()
    lastdatewithfine=models.DateField()