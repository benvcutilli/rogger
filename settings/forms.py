from django import forms

class ShoeForm(forms.Form):
    shoeName = forms.CharField(max_length=100)
