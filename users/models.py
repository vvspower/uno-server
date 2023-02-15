from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

# Create your models here.

class User(AbstractUser):
    bio = models.CharField(max_length=200, null=True)
    rank = models.CharField(max_length=100, null=True)
    elo = models.IntegerField(null=True)
    email = models.EmailField(null=True, unique=True)
    avatar = models.CharField(max_length=400, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']