from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Workout(models.Model):
    distance                =   models.DecimalField(max_digits=20, decimal_places=4)
    # next line citation [16]
    shoe                    =   models.ForeignKey('settings.Shoe', on_delete=models.SET_NULL, null=True)
    entry                   =   models.TextField(default="")
    hours                   =   models.DecimalField(max_digits=20, decimal_places=4, null=True)
    minutes                 =   models.DecimalField(max_digits=20, decimal_places=4, null=True)
    seconds                 =   models.DecimalField(max_digits=20, decimal_places=4, null=True)
    # type/subtype from Merv
    # next line citation [16]
    wtype                   =   models.ForeignKey('settings.WorkoutType', null=True, on_delete=models.SET_NULL)
    backupType              =   models.CharField(max_length=50, null=True)
    # THESE NEXT SEVEN ARE NOT USED IN ROGGER OTHER THAN TO SAVE MERV/OLD ROGGER DATA FOR POTENTIAL LATER USE
    mervOldRoggerLegacyType =   models.CharField(max_length=100, null=True)
    mervLegacySubtype       =   models.CharField(max_length=100, null=True)
    mervLegacyPace          =   models.CharField(max_length=100, null=True)
    mervLegacyPaceUnits     =   models.CharField(max_length=50, null=True)
    mervLegacyHeartrate     =   models.DecimalField(max_digits=20, decimal_places=4, null=True)
    mervLegacyAddendum      =   models.CharField(max_length=100, null=True)
    mervLegacyDistance      =   models.DecimalField(max_digits=20, decimal_places=4, null=True)
    mervLegacyDistanceUnits =   models.CharField(max_length=30, null=True)
    title                   =   models.CharField(max_length=100, default="")
    modifiedDate            =   models.DateTimeField()
    date                    =   models.DateField(default=date(1970,1,1)) # DEFAULT IS UNIX EPOCH
    updated                 =   models.BooleanField(default=False)
    # mervImport FROM THE PREVIOUS VERSION OF ROGGER (I don't think this idea came from an outside resource, but I'm not sure)
    mervImport              =   models.BooleanField(default=False)
    # oldRoggerTransfer IS INSPIRED BY mervImport, WHICH IS FROM THE PREVIOUS VERSION OF ROGGER (I don't think the mervImport idea came from an outside resource, but I'm not sure)
    oldRoggerTransfer       =   models.BooleanField(default=False)

    owner                   =   models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def getEscapedEntry(self):
        # (NOTE: THIS CITATION DOES NOT APPLY HERE, BUT KEEPING IT HERE JUST IN CASE I NEED IT BACK AGAIN): next line citation [18]
        return self.entry


class Comment(models.Model):
    commentText     =   models.TextField()
    owner           =   models.ForeignKey(User, on_delete=models.CASCADE)
    workout         =   models.ForeignKey(Workout, on_delete=models.CASCADE)
    dateAndTime     =   models.DateTimeField()


class Unit(models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name        = models.CharField(max_length=100)
    distance    = models.DecimalField(max_digits=20, decimal_places=4)
