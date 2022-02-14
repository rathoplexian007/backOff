from statistics import mode
from django.db import models

# Create your models here.
class Officials(models.Model):
    id=models.AutoField(primary_key=True)
    official_gmail=models.EmailField(null=False, unique=True, max_length=255)
    official_account=models.CharField(null=False, unique=True, max_length=255,default='')
    available_time=models.DateTimeField()

class User(models.Model):
    id=models.AutoField(primary_key=True)
    blockchain_address=models.CharField(null=False, unique=True, max_length=255,default='')
    kyc_done=models.BooleanField(null=False,default=False)
    official_appointed=models.BooleanField(null=False,default=False)

class Meeting(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,unique=False,null=True)
    official=models.ForeignKey(Officials,on_delete=models.CASCADE,unique=False,null=True)
    pending=models.BooleanField(null=False, default=True)
    meetlink=models.CharField(unique=False,null=True,max_length=40)
    meetingTime=models.DateTimeField()