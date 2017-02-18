from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Workout(models.Model):
    distance                =   models.FloatField()
    # next line citation [16]
    shoe                    =   models.ForeignKey('settings.Shoe', on_delete=models.SET_NULL, null=True)
    entry                   =   models.TextField(default="")
    hours                   =   models.FloatField(null=True)
    minutes                 =   models.FloatField(null=True)
    seconds                 =   models.FloatField(null=True)
    # type/subtype from Merv
    # next line citation [16]
    wtype                   =   models.ForeignKey('settings.WorkoutType', null=True, on_delete=models.SET_NULL)
    # THESE NEXT SEVEN ARE NOT USED IN ROGGER OTHER THAN TO SAVE MERV DATA FOR POTENTIAL LATER USE
    mervLegacySubtype       =   models.CharField(max_length=100, null=True)
    mervLegacyPace          =   models.CharField(max_length=100, null=True)
    mervLegacyPaceUnits     =   models.CharField(max_length=50, null=True)
    mervLegacyHeartrate     =   models.IntegerField(null=True)
    mervLegacyAddendum      =   models.CharField(max_length=100, null=True)
    mervLegacyDistance      =   models.FloatField(null=True)
    mervLegacyDistanceUnits =   models.CharField(max_length=30, null=True)
    title                   =   models.CharField(max_length=100, default="")
    modifiedDate            =   models.DateTimeField()
    date                    =   models.DateField(default=date(1970,1,1)) # DEFAULT IS UNIX EPOCH
    updated                 =   models.BooleanField(default=False)
    # mervImport FROM THE PREVIOUS VERSION OF ROGGER (I don't think this idea came from an outside resource, but I'm not sure)
    mervImport              =   models.BooleanField(default=False)

    owner                   =   models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def getEscapedEntry(self):
        # next line citation [18]
        return self.entry.encode("unicode_escape")


class Comment(models.Model):
    commentText     =   models.TextField()
    owner           =   models.ForeignKey(User, on_delete=models.CASCADE)
    workout         =   models.ForeignKey(Workout, on_delete=models.CASCADE)
    dateAndTime     =   models.DateTimeField(auto_now=True)
