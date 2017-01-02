from django import forms
from workoutLogging.models import Workout

class ShoeForm(forms.Form):
    name = forms.CharField(max_length=100)

    
