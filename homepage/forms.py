from django import forms

class CreateAccountForm(forms.Form):
    username                = forms.CharField()
    password                = forms.CharField()
    passwordConfirmation    = forms.CharField()
    emailAddress            = forms.EmailField()
