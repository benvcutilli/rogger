from django.db import models


# Create your models here.
class Workout(models.Model):
    distance    =   models.FloatField()
    # next line citation [16]
    shoe        =   models.ForeignKey('settings.Shoe', on_delete=models.SET_NULL, null=True)
