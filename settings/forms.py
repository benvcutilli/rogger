from django import forms
from workoutLogging.models import Workout

class ShoeForm(forms.Form):
    name = forms.CharField(max_length=100)

class AccountSettingsForm(forms.Form):
    emailAddress        =   forms.EmailField(required=False)
    displayName         =   forms.CharField(max_length=100, required=False)
    privacySelection    =   forms.IntegerField()
