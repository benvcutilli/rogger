from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from workoutLogging import forms
from settings.models import Shoe, WorkoutType
from workoutLogging.models import Workout

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
    availableWorkoutTypes = WorkoutType.objects.filter(owner__isnull=True) | WorkoutType.objects.filter(owner=request.user)
    templateDict.update({
        'formURL'   :   reverse("newEntryView"),
        'error'     :   "",
        'shoes'     :   [(element, repr(element.id)) for element in Shoe.objects.filter(owner=request.user)],
        'types'     :   [(element, repr(element.id)) for element in availableWorkoutTypes]
    })



    if request.user.is_authenticated:
        workoutForm = forms.WorkoutForm({
            'title'     :   "",
            'distance'  :   "0 miles",
            'hours'     :   "",
            'minutes'   :   "",
            'seconds'   :   "",
            'wtype'     :   "",
            'shoe'      :   "",
            'entry'     :   "",
            'date'      :   "",
        })
        if request.method == "POST":
            workoutForm = forms.WorkoutForm({
                'title'     :   request.POST['title'],
                'distance'  :   request.POST['distance'],
                'hours'     :   request.POST['hours'],
                'minutes'   :   request.POST['minutes'],
                'seconds'   :   request.POST['seconds'],
                'wtype'     :   request.POST['type'],
                'shoe'      :   request.POST['shoe'],
                'entry'     :   request.POST['entryText'],
                'date'      :   request.POST['date'],
            })
            print([workoutForm['shoe'].data == shoe.id for shoe in Shoe.objects.filter(owner=request.user)])
            if workoutForm.is_valid():
                workout = Workout.objects.create(
                    title       =   workoutForm.cleaned_data['title'],
                    distance    =   workoutForm.cleaned_data['distance'],
                    hours       =   workoutForm.cleaned_data['hours'],
                    minutes     =   workoutForm.cleaned_data['minutes'],
                    seconds     =   workoutForm.cleaned_data['seconds'],
                    wtype       =   WorkoutType.objects.get(id=int(workoutForm.cleaned_data['wtype'])),
                    shoe        =   Shoe.objects.get(id=workoutForm.cleaned_data['shoe']) if workoutForm.cleaned_data['shoe'] >= 0 else None,
                    entry       =   workoutForm.cleaned_data['entry'],
                    owner       =   request.user,
                    date        =   workoutForm.cleaned_data['date']
                )

                workout.save()
                return HttpResponseRedirect(reverse("homepage"))
            else:
                templateDict['error'] = workoutForm.getErrorString()

        templateDict.update({
            'form': workoutForm
        })
        return render(request, "workoutLogging/newentry.html", templateDict)
    else:
        return HttpResponseForbidden()

def editEntry(request, workoutID):
    templateDict = entryLocalization[debugLocale]
    availableWorkoutTypes = WorkoutType.objects.filter(owner__isnull=True) | WorkoutType.objects.filter(owner=request.user)
    templateDict.update({
        'formURL'   :   reverse("editEntryView", args=[workoutID]),
        'error'     :   "",
        'shoes'     :   [(element, repr(element.id)) for element in Shoe.objects.filter(owner=request.user)],
        'types'     :   [(element, repr(element.id)) for element in availableWorkoutTypes]
    })
    workout = Workout.objects.get(id=int(workoutID))
    workoutForm = forms.WorkoutForm({
        'title'     :   workout.title,
        'distance'  :   repr(workout.distance),
        'hours'     :   repr(workout.hours) if workout.hours != None else "",
        'minutes'   :   repr(workout.minutes) if workout.minutes != None else "",
        'seconds'   :   repr(workout.seconds) if workout.seconds != None else "",
        'wtype'     :   repr(workout.wtype.id),
        'shoe'      :   repr(workout.shoe.id) if workout.shoe != None else "-1",
        'entry'     :   workout.entry,
        'date'      :   repr(workout.date.year) + "." + ("0" if workout.date.month < 10 else "") + repr(workout.date.month) + "." + ("0" if workout.date.day < 10 else "") + repr(workout.date.day),
    })

    if request.method == "POST":
        workoutForm = forms.WorkoutForm({
            'title'     :   request.POST['title'],
            'distance'  :   request.POST['distance'],
            'hours'     :   request.POST['hours'],
            'minutes'   :   request.POST['minutes'],
            'seconds'   :   request.POST['seconds'],
            'wtype'     :   request.POST['type'],
            'shoe'      :   request.POST['shoe'],
            'entry'     :   request.POST['entryText'],
            'date'      :   request.POST['date'],
        })
        if workoutForm.is_valid():
            workout = Workout.objects.get(id=workoutID)

            workout.title       =   workoutForm.cleaned_data['title'],
            workout.distance    =   workoutForm.cleaned_data['distance'],
            workout.hours       =   workoutForm.cleaned_data['hours'],
            workout.minutes     =   workoutForm.cleaned_data['minutes'],
            workout.seconds     =   workoutForm.cleaned_data['seconds'],
            workout.wtype       =   WorkoutType.objects.get(id=int(workoutForm.cleaned_data['wtype'])),
            workout.shoe        =   Shoe.objects.get(id=workoutForm.cleaned_data['shoe']) if workoutForm.cleaned_data['shoe'] >= 0 else None,
            workout.entry       =   workoutForm.cleaned_data['entry'],
            workout.owner       =   request.user,
            workout.date        =   workoutForm.cleaned_data['date']
            workout.updated     =   True


            workout.save()
            return HttpResponseRedirect(reverse("homepage"))

    templateDict.update({
        'form'  :   workoutForm
    })
    return render(request, "workoutLogging/editentry.html", templateDict)

def viewEntry(request):
    return render(request, "workoutLogging/viewentry.html", entryLocalization[debugLocale])
