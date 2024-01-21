from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    number = models.CharField(max_length=20)
    height = models.IntegerField()
    weight = models.IntegerField()
    location = models.CharField(max_length=100)