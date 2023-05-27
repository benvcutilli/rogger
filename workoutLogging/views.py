from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from workoutLogging import forms
from settings.models import Shoe, WorkoutType
from workoutLogging.models import Workout, Comment, Unit
from django.core.mail import send_mail
from shared.models import Block, Follow
import datetime
from django.shortcuts import get_object_or_404
from copy import deepcopy
import re
from django.contrib.auth.models import User

import shared.tools

debugLocale = 'english'

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

usernameRegex = re.compile(r'@([0-9a-zA-Z_]+)(?:\W|\Z)')

# Create your views here.

def newEntry(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginView"))
    templateDict = deepcopy(entryLocalization[debugLocale])
    availableWorkoutTypes = None
    if WorkoutType.objects.filter(owner=request.user).count() > 1:
        availableWorkoutTypes = WorkoutType.objects.filter(owner__isnull=True) | WorkoutType.objects.filter(owner=request.user).exclude(name="Unknown")
    else:
        availableWorkoutTypes = WorkoutType.objects.filter(owner__isnull=True) | WorkoutType.objects.filter(owner=request.user)

    templateDict.update({
        'formURL'       :   reverse("newEntryView"),
        'error'         :   "",
        'shoes'         :   [(element, str(element.id)) for element in Shoe.objects.filter(owner=request.user)],
        'types'         :   [(element, str(element.id)) for element in availableWorkoutTypes],
        # NEXT LINE: THE STORING OF newWorkoutDate IN THE SESSION FOR TEMPORARY HOLDING BETWEEN WEBPAGES FROM CITATION [25]
        'workoutDate'   :   request.session['newWorkoutDate'] if request.session.has_key('newWorkoutDate') else datetime.date.today().strftime("%Y.%m.%d"),
        'units'         :   (Unit.objects.filter(owner=request.user) | Unit.objects.filter(owner=None)).order_by("-name")
    })



    # NEXT LINES: THE STORING (AND NOW DELETION) OF newWorkoutDate IN THE SESSION FOR TEMPORARY HOLDING BETWEEN WEBPAGES FROM CITATION [25]
    if request.session.has_key('newWorkoutDate'):
        del request.session['newWorkoutDate']
    # END CITATION



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
                    title           =   workoutForm.cleaned_data['title'],
                    distance        =   workoutForm.cleaned_data['distance'],
                    hours           =   workoutForm.cleaned_data['hours'],
                    minutes         =   workoutForm.cleaned_data['minutes'],
                    seconds         =   workoutForm.cleaned_data['seconds'],
                    wtype           =   WorkoutType.objects.get(id=int(workoutForm.cleaned_data['wtype'])),
                    shoe            =   Shoe.objects.get(id=workoutForm.cleaned_data['shoe']) if workoutForm.cleaned_data['shoe'] >= 0 else None,
                    entry           =   workoutForm.cleaned_data['entry'],
                    owner           =   request.user,
                    date            =   workoutForm.cleaned_data['date'],
                    modifiedDate    =   datetime.datetime.now()
                )

                workout.save()

                global usernameRegex
                usernames = list(
                                set(
                                    usernameRegex.findall(
                                        workoutForm.cleaned_data['entry']
                                    )
                                )
                            )
                ignore = Block.objects.filter(blockee=request.user).values_list("blocker__id", flat=True)
                # This line (in part) achieves the goal [256] of not emailing the user if they don't want to be emailed
                tagged = User.objects.filter(username__in=usernames).exclude(pk__in=ignore).exclude(userinfo__emailOnActivity=False)
                shared.tools.blastEmail(
                            "alertbot@rogger.co",
                            "You were tagged in an entry located at https://rogger.co" + reverse("viewEntryView", args=[workout.id]),
                            "You were tagged in an entry",
                            tagged
                )

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
    workout = get_object_or_404(Workout, id=int(workoutID))
    templateDict = deepcopy(entryLocalization[debugLocale])
    availableWorkoutTypes = WorkoutType.objects.filter(owner__isnull=True) | (WorkoutType.objects.filter(owner=request.user).exclude(name="Unknown") if workout.wtype.name != "Unknown" else WorkoutType.objects.filter(owner=request.user))
    templateDict.update({
        'formURL'   :   reverse("viewEntryView", args=[workoutID]),
        'error'     :   "",
        'shoes'     :   [(element, str(element.id)) for element in Shoe.objects.filter(owner=request.user)],
        'types'     :   [(element, str(element.id)) for element in availableWorkoutTypes],
        'units'     :   (Unit.objects.filter(owner=request.user) | Unit.objects.filter(owner=None)).order_by("-name")
    })

    workoutForm = forms.WorkoutForm({
        'title'     :   workout.title,
        'distance'  :   str(workout.distance),
        'hours'     :   str(workout.hours) if workout.hours != None else "",
        'minutes'   :   str(workout.minutes) if workout.minutes != None else "",
        'seconds'   :   str(workout.seconds) if workout.seconds != None else "",
        'wtype'     :   str(workout.wtype.id),
        'shoe'      :   str(workout.shoe.id) if workout.shoe != None else "-1",
        'entry'     :   workout.entry,
        'date'      :   str(workout.date.year) + "." + ("0" if workout.date.month < 10 else "") + str(workout.date.month) + "." + ("0" if workout.date.day < 10 else "") + str(workout.date.day),
    })

    isError = False
    error = ""
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
            workout = get_object_or_404(Workout, id=workoutID)
            if workoutForm.is_valid():

                global usernameRegex
                usernames = list(
                                set(
                                    usernameRegex.findall(
                                        workoutForm.cleaned_data['entry']
                                    )
                                )
                            )
                ignore = Block.objects.filter(blockee=request.user).values_list("blocker__id", flat=True)
                # emailOnActivity is filtered here because of [256]
                tagged = User.objects.filter(username__in=usernames).exclude(pk__in=ignore).exclude(userinfo__emailOnActivity=False)
                shared.tools.blastEmail(
                            "alertbot@rogger.co",
                            "You were tagged in an entry located at https://rogger.co" + reverse("viewEntryView", args=[workout.id]),
                            "You were tagged in an entry",
                            tagged
                )

                workout.title           =   workoutForm.cleaned_data['title']
                workout.distance        =   workoutForm.cleaned_data['distance']
                workout.hours           =   workoutForm.cleaned_data['hours']
                workout.minutes         =   workoutForm.cleaned_data['minutes']
                workout.seconds         =   workoutForm.cleaned_data['seconds']
                workout.wtype           =   WorkoutType.objects.get(id=int(workoutForm.cleaned_data['wtype']))
                workout.shoe            =   Shoe.objects.get(id=workoutForm.cleaned_data['shoe']) if workoutForm.cleaned_data['shoe'] >= 0 else None
                workout.entry           =   workoutForm.cleaned_data['entry']
                workout.owner           =   request.user
                workout.date            =   workoutForm.cleaned_data['date']
                workout.updated         =   True
                workout.modifiedDate    =   datetime.datetime.now()


                workout.save()

                return HttpResponseRedirect(reverse("homepage"))
            else:
                isError = True
                error = workoutForm.errors
                print(workoutForm.errors)
        else:
            workout.delete()
            return HttpResponseRedirect(reverse("homepage"))
        # END CITATION

    templateDict.update({
        'isError'           :   isError,
        'error'             :   error,
        'form'              :   workoutForm,
        'escapedEntry'      :   workout.getEscapedEntry(),
        'workoutID'         :   workoutID,
        'viewRenderMode'    :   False,
        'comments'          :   Comment.objects.filter(workout=workout)
    })
    return render(request, "workoutLogging/editentry.html", templateDict)

def viewEntry(request, workoutID):
    workout = get_object_or_404(Workout, id=workoutID)
    if request.user == workout.owner:
        return editEntry(request, workoutID)
    if request.user != workout.owner and workout.owner.userinfo.privacySelection == 2:
        # usage of the "approved" attribute in a Follow object from citation [25]
        if not (request.user.is_authenticated and Follow.objects.filter(followee=workout.owner, follower=request.user, approved=True).exists()) or not request.user.is_authenticated:
            return HttpResponseNotFound()
    if (request.user != workout.owner and workout.owner.userinfo.privacySelection == 3) or (request.user.is_authenticated and Block.objects.filter(blockee=request.user, blocker=workout.owner)):
        return HttpResponseNotFound()
    workoutInfo = {
        'title'     :   workout.title,
        'distance'  :   str(workout.distance),
        'hours'     :   str(workout.hours.normalize()) if workout.hours != None else "",
        'minutes'   :   str(workout.minutes.normalize()) if workout.minutes != None else "",
        'seconds'   :   str(workout.seconds.normalize()) if workout.seconds != None else "",
        'wtype'     :   str(workout.wtype.id),
        'shoe'      :   workout.shoe,
        'entry'     :   workout.entry,
        'date'      :   str(workout.date.year) + "." + ("0" if workout.date.month < 10 else "") + str(workout.date.month) + "." + ("0" if workout.date.day < 10 else "") + str(workout.date.day),
        'username'  :   workout.owner.username
    }
    templateDict = {

        'escapedEntry'      :   workout.getEscapedEntry(),
        'workoutID'         :   workoutID,
        'info'              :   workoutInfo,
        'viewRenderMode'    :   True,
        'comments'          :   Comment.objects.filter(workout=workout).exclude(owner__in=[block.blockee for block in Block.objects.filter(blocker=request.user)]) if request.user.is_authenticated else Comment.objects.filter(workout=workout),
        'error'             :   ""
    }

    templateDict.update(entryLocalization[debugLocale])
    return render(request, "workoutLogging/viewentry.html", templateDict)



def commentAddView(request, workoutID):

    workout = get_object_or_404(Workout, id=workoutID)

    if workout.owner.userinfo.privacySelection == 3:
        return HttpResponseNotFound()

    # usage of the "approved" attribute in a Follow object from citation [25]
    if (workout.owner.userinfo.privacySelection == 2 and not (Follow.objects.filter(followee=workout.owner, follower=request.user, approved=True).exists() or workout.owner == request.user)) or (workout.owner.userinfo.privacySelection == 3 and not workout.owner == request.user):
        return HttpResponseNotFound()

    if request.user.is_authenticated:

        commentText = request.POST['text']
        newComment = Comment.objects.create(commentText=commentText, owner=request.user, workout=workout, dateAndTime=datetime.datetime.now())
        newComment.save()

        sendTo = []
        for comment in Comment.objects.filter(workout=workout):
            if request.user != comment.owner:
                if comment.owner.userinfo.emailOnActivity:
                    sendTo.append(comment.owner)
        # See [256] for the reason for the second part of the "if" in this line
        sendTo = ([workout.owner] if (workout.owner != request.user and workout.owner.userinfo.emailOnActivity) else []) + sendTo
        shared.tools.blastEmail("alertbot@rogger.co", "See the comment at https://rogger.co" + reverse("viewEntryView", args=[workoutID]), "Someone posted a comment on a workout with which you have interacted", sendTo)

        return render(request, "workoutLogging/comment.html", { 'comment' : newComment })

    else:
        return HttpResponseForbidden("Please log in to use this feature.")

def commentDeleteView(request, workoutID):
    if request.user.is_authenticated:
        commentID = request.POST['id']
        comment = get_object_or_404(Comment, id=int(commentID))
        if request.user == comment.owner:
            comment.delete()
            return HttpResponse("")
        else:
            # usage of the "approved" attribute in a Follow object from citation [25]
            if comment.owner.userinfo.privacySelection == 3 or (comment.owner.userinfo.privacySelection == 2 and not Follow.objects.filter(followee=comment.owner, follower=request.user, approved=True).exists()):
                return HttpResponseNotFound("This comment isn't available. It may not exist.")
            return HttpReponseForbidden("You don't own this comment, so you can't delete it.")
    else:
        return HttpResponseForbidden("Please log in to use this feature")

# THIS METHOD, USED IN THE FUNCTION storeDate BELOW, OF STORING THE DATE (FOR A NEW LOG ENTRY) IN THE USER'S SESSION FROM
# CITATION [25]
def storeDate(request):
    if not request.user.is_authenticated:
        return HttpReponseForbidden()


    request.session['newWorkoutDate'] = request.POST['entryDate']
    return HttpResponse()
