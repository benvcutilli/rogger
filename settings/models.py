from django.db import models
from shared.models import UserInfo
from workoutLogging.models import Workout
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

class Shoe(models.Model):
    name        = models.CharField(max_length=100)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def mileage(self):
        workouts = Workout.objects.filter(shoe=self)
        totalMileage = Decimal('0.0')
        for workout in workouts:
            totalMileage += workout.distance

        return totalMileage

# USING "Workout" AND "Type" TO CREATE "WorkoutType" AS A NAME IS INSPIRED BY CITATION [43]
class WorkoutType(models.Model):
    owner               =   models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name                =   models.CharField(max_length=50)
    displayMeasurement  =   models.IntegerField(default=0)
