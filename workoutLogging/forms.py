from django import forms

class WorkoutForm(forms.Form):
    title           =   forms.CharField(max_length=100)
    distance        =   forms.FloatField()
    hours           =   forms.IntegerField(required=False)
    minutes         =   forms.IntegerField(required=False)
    seconds         =   forms.FloatField(required=False)
    # type/subtype from Merv
    wtype           =   forms.CharField(max_length=50)
    wsubtype        =   forms.CharField(max_length=50)
    shoe            =   forms.IntegerField(required=False)
    entry           =   forms.CharField()
    date           =   forms.DateField(input_formats=["%Y.%m.%d"])

    def getErrorString(self):
        errorString = ""
        for key in self.errors:
            errorString += key + ": " + ", ".join([self.errors[key][i] for i in range(len(self.errors[key]))]) + " "

        return errorString

    def getEscapedEntry(self):
        return self['entry'].data.replace("\\", "\\\\").replace("\"", "\\\"")
