from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.urls import reverse
from django.http import HttpResponseForbidden
from workoutLogging import forms
from settings.models import Shoe

debugLocale = 'french'

entryFrenchDict = {
}
entryFrenchDict.update(baseLocalization['french'])

entryEnglishDict = {
}
entryEnglishDict.update(baseLocalization['english'])

entryLocalization = {
    'french'    :   entryFrenchDict,
    'english'   :   entryEnglishDict,
}

# Create your views here.

def newEntry(request):
    templateDict = entryLocalization[debugLocale]
    templateDict.update({
        'formURL'   :   reverse("newEntryView"),
        'error'     :   ""
    })

    if request.user.is_authenticated:
        if request.method = "POST":
            workoutForm = forms.WorkoutForm({
                'title'     :   request.POST['title'],
                'distance'  :   request.POST['distance'],
                'hours'     :   request.POST['durationHours'],
                'minutes'   :   request.POST['durationMinutes'],
                'seconds'   :   request.POST['durationSeconds'],
                'wtype'     :   request.POST['type'],
                'wsubtype'  :   request.POST['subtype'],
                'shoe'      :   request.POST['shoe'],
                'entry'     :   request.POST['entryText']
            })

            if workoutForm.is_valid():
                workout = Workout.object.create(
                    title       =   workoutForm.cleaned_data['title'],
                    distance    =   workoutForm.cleaned_data['distance'],
                    hours       =   workoutForm.cleaned_data['hours'],
                    minutes     =   workoutForm.cleaned_data['minutes'],
                    seconds     =   workoutForm.cleaned_data['seconds'],
                    wtype       =   workoutForm.cleaned_data['wtype'],
                    wsubtype    =   workoutForm.cleaned_data['wsubtype'],
                    shoe        =   Shoe.objects.get(id=workoutForm.cleaned_data['shoe']),
                    entry       =   workoutForm.cleaned_data['entry'],
                    owner       =   request.user
                )

                workout.save()
                return HttpResponseRedirect(reverse("homepage"))
            else:
                templateDict['error'] = workoutForm.getErrorString()
        return render(request, "workoutLogging/newentry.html", templateDict)
    else:
        return HttpResponseForbidden()

def editEntry(request):
    return render(request, "workoutLogging/editentry.html", entryLocalization[debugLocale])

def viewEntry(request):
    return render(request, "workoutLogging/viewentry.html", entryLocalization[debugLocale])
