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

universalWorkoutTypeNames = [
    # FOLLOWING ARE FROM AND/OR INSPIRED BY MERV
    ("Easy Run",    0),
    ("Tempo",       0),
    ("Repeats",     0),
    ("Bike",        0),
    ("Cross Train", 1),
    ("Swim",        0),
    # FOLLOWING ARE DEFINITELY FROM MERV
    ("Weights",     0),
    ("Rower",       1),
    ("Stepper",     0),
    ("Skate",       0),
    ("Walk",        0),
    ("Ski",         0),
    ("Steady Run",  0),
    ("Hill Run",    0),
    ("Fartlek",     0),
    ("Race",        0),

]

universalWorkoutTypeNames = universalWorkoutTypeNames[-4:] + universalWorkoutTypeNames[:-4]

class WorkoutType(models.Model):
    owner               =   models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name                =   models.CharField(max_length=50)
    displayMeasurement  =   models.IntegerField(default=0)
