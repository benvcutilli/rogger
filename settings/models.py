from django.db import models
from shared.models import UserInfo
from workoutLogging.models import Workout
from django.contrib.auth.models import User

# Create your models here.

class Shoe(models.Model):
    name        = models.CharField(max_length=100)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def mileage(self):
        workouts = Workout.objects.filter(shoe=self)
        totalMileage = 0.0
        for workout in workouts:
            totalMileage += workout.distance

        return totalMileage
