# This file and the next line likely created by django-admin startapp
# [79, "startapp" documentation]
from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CreateAccountForm(forms.Form):
    username                = forms.CharField(label="username")
    password                = forms.CharField(label="password")
    passwordConfirmation    = forms.CharField(label="confirm password")
    emailAddress            = forms.EmailField(label="email address")
    formTranslation = {
        'passwordConfirmation'  :   "password confirmation",
        'password'              :   "password",
        'username'              :   "username",
        'emailAddress'          :   "email address"
    }

class LoginForm(forms.Form):
    username                = forms.CharField(label="username")
    password                = forms.CharField(label="password")
    formTranslation = {
        'password'              :   "password",
        'username'              :   "username",
    }

class ChangePasswordForm(forms.Form):
    newPassword             =   forms.CharField()
    newPasswordConfirmation =   forms.CharField()
    oldPassword             =   forms.CharField()

class RoggerSetPasswordForm(SetPasswordForm):
    def getErrorString():
        errorString = ""
        for key in self.errors:
            errorString += key + ": " + ", ".join([self.errors[key][i] for i in range(len(self.errors[key]))])

        return errorString
