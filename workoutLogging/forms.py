from django import forms

class WorkoutForm(forms.Form):
    title           =   forms.CharField(max_length=100)
    distance        =   forms.FloatField()
    hours           =   forms.FloatField()
    minutes         =   forms.FloatField()
    seconds         =   forms.FloatField()
    # type/subtype from Merv
    wtype           =   forms.CharField(max_length=50)
    subtype         =   forms.CharField(max_length=50)
    shoe            =   forms.IntegerField()
    entry           =   forms.TextField()
