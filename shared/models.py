from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    # next line from citation [14]
    authUser            =   models.OneToOneField(User, on_delete=models.CASCADE)
    displayName         =   models.CharField(max_length=100, default="")
    privacySelection    =   models.IntegerField(default=1)
