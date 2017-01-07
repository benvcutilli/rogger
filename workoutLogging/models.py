from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Workout(models.Model):
    distance    =   models.FloatField()
    # next line citation [16]
    shoe            =   models.ForeignKey('settings.Shoe', on_delete=models.SET_NULL, null=True)
    entry           =   models.TextField(default="")
    hours           =   models.FloatField(null=True)
    minutes         =   models.FloatField(null=True)
    seconds         =   models.FloatField(null=True)
    # type/subtype from Merv
    # next line citation [16]
    wtype           =   models.ForeignKey('settings.WorkoutType', null=True)
    title           =   models.CharField(max_length=100, default="")
    modifiedDate    =   models.DateTimeField(auto_now=True)
    date            =   models.DateField(default=date(1970,1,1)) # DEFAULT IS UNIX EPOCH
    updated         =   models.BooleanField(default=False)

    owner           =   models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    commentText     =   models.TextField()
    owner           =   models.ForeignKey(User, on_delete=models.CASCADE)
    workout         =   models.ForeignKey(Workout, on_delete=models.CASCADE)
    dateandtime     =   models.DateTimeField(auto_now=True)
