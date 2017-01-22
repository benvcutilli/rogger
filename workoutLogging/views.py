from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from workoutLogging import forms
from settings.models import Shoe, WorkoutType
from workoutLogging.models import Workout, Comment
from django.core.mail import send_mail

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
            'form': workoutForm,
            'escapedEntry'  :   "",
            'viewRenderMode':   False
        })
        return render(request, "workoutLogging/newentry.html", templateDict)
    else:
        return HttpResponseForbidden()

def editEntry(request, workoutID):
    workout = Workout.objects.get(id=int(workoutID))
    templateDict = entryLocalization[debugLocale]
    availableWorkoutTypes = WorkoutType.objects.filter(owner__isnull=True) | WorkoutType.objects.filter(owner=request.user)
    templateDict.update({
        'formURL'   :   reverse("viewEntryView", args=[workoutID]),
        'error'     :   "",
        'shoes'     :   [(element, repr(element.id)) for element in Shoe.objects.filter(owner=request.user)],
        'types'     :   [(element, repr(element.id)) for element in availableWorkoutTypes]
    })

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
        # THIS WHOLE IF/ELSE SEGMENT CONDITIONAL LINES FROM [17]
        if 'saveButton' in request.POST:
            workout = Workout.objects.get(id=workoutID)
            if workoutForm.is_valid():


                workout.title       =   workoutForm.cleaned_data['title']
                workout.distance    =   workoutForm.cleaned_data['distance']
                workout.hours       =   workoutForm.cleaned_data['hours']
                workout.minutes     =   workoutForm.cleaned_data['minutes']
                workout.seconds     =   workoutForm.cleaned_data['seconds']
                workout.wtype       =   WorkoutType.objects.get(id=int(workoutForm.cleaned_data['wtype']))
                workout.shoe        =   Shoe.objects.get(id=workoutForm.cleaned_data['shoe']) if workoutForm.cleaned_data['shoe'] >= 0 else None
                workout.entry       =   workoutForm.cleaned_data['entry']
                workout.owner       =   request.user
                workout.date        =   workoutForm.cleaned_data['date']
                workout.updated     =   True


                workout.save()
                return HttpResponseRedirect(reverse("homepage"))
        else:
            workout.delete()
            return HttpResponseRedirect(reverse("homepage"))
        # END CITATION

    templateDict.update({
        'error'             :   "",
        #'info'  :   workoutInfo,
        'form'              :   workoutForm,
        'escapedEntry'      :   workout.getEscapedEntry(),
        'workoutID'         :   workoutID,
        'viewRenderMode'    :   False,
        'comments'          :   Comment.objects.filter(workout=workout)
    })
    return render(request, "workoutLogging/editentry.html", templateDict)

def viewEntry(request, workoutID):
    workout = Workout.objects.get(id=workoutID)
    if request.user == workout.owner:
        return editEntry(request, workoutID)
    workoutInfo = {
        'title'     :   workout.title,
        'distance'  :   repr(workout.distance),
        'hours'     :   repr(workout.hours) if workout.hours != None else "",
        'minutes'   :   repr(workout.minutes) if workout.minutes != None else "",
        'seconds'   :   repr(workout.seconds) if workout.seconds != None else "",
        'wtype'     :   repr(workout.wtype.id),
        'shoe'      :   workout.shoe,
        'entry'     :   workout.entry,
        'date'      :   repr(workout.date.year) + "." + ("0" if workout.date.month < 10 else "") + repr(workout.date.month) + "." + ("0" if workout.date.day < 10 else "") + repr(workout.date.day),
        'username'  :   workout.owner.username
    }
    templateDict = {

        'escapedEntry'      :   workout.getEscapedEntry(),
        'workoutID'         :   workoutID,
        'info'              :   workoutInfo,
        'viewRenderMode'    :   True,
        'comments'          :   Comment.objects.filter(workout=workout),
        'error'             :   ""
    }
    #print(templateDict['escapedEntry'])
    templateDict.update(entryLocalization[debugLocale])
    return render(request, "workoutLogging/viewentry.html", templateDict)



def commentAddView(request, workoutID):
    workout = Workout.objects.get(id=workoutID)
    if request.user.is_authenticated:
        commentText = request.POST['text']
        otherEmails = []
        for comment in Comment.objects.filter(workout=workout):
            if request.user != comment.owner:
                otherEmails.append(comment.owner.email)
        emailRecipients = ([workout.owner.email] if workout.owner != request.user else []) + otherEmails
        send_mail("Some posted a comment on a workout with which you have interacted", "See the comment at https://rogger.co" + reverse("viewEntryView", args=[workoutID]), "alertbot@rogger.co", emailRecipients)
        newComment = Comment.objects.create(commentText=commentText, owner=request.user, workout=workout)
        newComment.save()

        return render(request, "workoutLogging/comment.html", { 'comment' : newComment })
    else:
        return HttpResponseForbidden("Please log in to use this feature.")

def commentDeleteView(request, workoutID):
    if request.user.is_authenticated:
        commentID = request.POST['id']
        comment = Comment.objects.get(id=int(commentID))
        if request.user == comment.owner:
            comment.delete()
            return HttpResponse("")
        else:
            return HttpReponseForbidden("You don't own this comment, so you can't delete it.")
    else:
        return HttpReponseForbidden("Please log in to use this feature")
