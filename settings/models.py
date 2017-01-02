from django.db import models
from shared.models import UserInfo
from workoutLogging.models import Workout

# Create your models here.

class Shoe(models.Model):
    name        = models.CharField(max_length=100)
    userInfo    = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def mileage(self):
        workouts = Workout.objects.filter(shoe=self)
        totalMileage = 0.0
        for workout in workouts:
            totalMileage += workout.distance

        return totalMileage
