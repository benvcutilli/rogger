from django import forms

class WorkoutForm(forms.Form):
    title           =   forms.CharField(max_length=100)
    distance        =   forms.FloatField()
    hours           =   forms.IntegerField()
    minutes         =   forms.IntegerField()
    seconds         =   forms.FloatField()
    # type/subtype from Merv
    wtype           =   forms.CharField(max_length=50)
    wsubtype        =   forms.CharField(max_length=50)
    shoe            =   forms.IntegerField()
    entry           =   forms.TextField()

    def getErrorString():
        errorString = ""
        for key in self.errors:
            errorString += key + ": " + ", ".join([self.errors[key][i] for i in range(len(self.errors[key]))])

        return errorString
