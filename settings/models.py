from django.db import models
from shared.models import UserInfo

# Create your models here.

class Shoe(models.Model):
    name        = models.CharField(max_length=100)
    userInfo    = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
