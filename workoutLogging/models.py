from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Workout(models.Model):
    distance    =   models.FloatField()
    # next line citation [16]
    shoe        =   models.ForeignKey('settings.Shoe', on_delete=models.SET_NULL, null=True)
    entry       =   models.TextField()
    hours       =   models.FloatField()
    minutes     =   models.FloatField()
    seconds     =   models.FloatField()
    # type/subtype from Merv
    wtype       =   models.CharField(max_length=50)
    wsubtype    =   models.CharField(max_length=50, null=True)
    title       =   models.CharField(max_length=100)

    owner       =   models.ForeignKey(User, on_delete=models.CASCADE)
