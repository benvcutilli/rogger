from django import forms

class WorkoutForm(forms.Form):
    title           =   forms.CharField(max_length=100)
    distance        =   forms.DecimalField()
    hours           =   forms.IntegerField(required=False)
    minutes         =   forms.IntegerField(required=False)
    seconds         =   forms.DecimalField(required=False)
    # type/subtype from Merv
    wtype           =   forms.IntegerField()
    shoe            =   forms.IntegerField(required=False)
    entry           =   forms.CharField(required=False)
    date            =   forms.DateField(input_formats=["%Y.%m.%d"])

    def getErrorString(self):
        errorString = ""
        for key in self.errors:
            errorString += key + ": " + ", ".join([self.errors[key][i] for i in range(len(self.errors[key]))]) + " "

        return errorString
