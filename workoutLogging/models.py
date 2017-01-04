from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Workout(models.Model):
    distance    =   models.FloatField()
    # next line citation [16]
    shoe        =   models.ForeignKey('settings.Shoe', on_delete=models.SET_NULL, null=True)
    entry       =   models.TextField(default="")
    hours       =   models.FloatField(null=True)
    minutes     =   models.FloatField(null=True)
    seconds     =   models.FloatField(null=True)
    # type/subtype from Merv
    wtype       =   models.CharField(max_length=50, default="")
    wsubtype    =   models.CharField(max_length=50, null=True)
    title       =   models.CharField(max_length=100, default="")

    owner       =   models.ForeignKey(User, on_delete=models.CASCADE, null=True)
