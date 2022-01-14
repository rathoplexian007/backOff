from django.db import models

# Create your models here.

class User(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField(null=False, unique=True, max_length=255)
    password=models.CharField(null=False, max_length=255)