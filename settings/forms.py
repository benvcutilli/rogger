from django import forms

class ShoeForm(forms.Form):
    name = forms.CharField(max_length=100)
