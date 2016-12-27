from django import forms

class CreateAccountForm(forms.Form):
    username                = forms.CharField(label="username")
    password                = forms.CharField(label="password")
    passwordConfirmation    = forms.CharField(label="confirm password")
    emailAddress            = forms.EmailField(label="email address")
