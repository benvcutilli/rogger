# This file and the next line likely created by django-admin startapp
# [79, "startapp" documentation]
from django import forms
from workoutLogging.models import Workout

class ShoeForm(forms.Form):
    name = forms.CharField(max_length=100)

class AccountSettingsForm(forms.Form):
    emailAddress        =   forms.EmailField(required=False)
    displayName         =   forms.CharField(max_length=100, required=False)
    privacySelection    =   forms.IntegerField()
    pdfName             =   forms.CharField(max_length=100, required=False)
    #searchUsername      =   forms.BooleanField()
    #searchDisplayName   =   forms.BooleanField()

# The form used to import Merv[70] export data:
class ImportForm(forms.Form):
    mervData = forms.CharField()
