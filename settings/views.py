from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.urls import reverse
from settings.forms import ShoeForm, AccountSettingsForm
from settings.models import Shoe, WorkoutType
from django.contrib.auth import authenticate
import datetime
from settings.forms import ImportForm
import re
from workoutLogging.models import Workout

# Create your views here.

baseLocale = 'french'

settingsFrenchDict = {
}
settingsFrenchDict.update(baseLocalization['french'])

settingsEnglishDict = {
}
settingsEnglishDict.update(baseLocalization['english'])

localizationDict = {
    'french'    :   settingsFrenchDict,
    'english'   :  settingsEnglishDict,
}

def settings(request):

    def settingsAJAX(request):
        if request.POST['todo'] == "addShoe":
            shoeForm = ShoeForm({
                'name'  :   request.POST['newShoeName'],
            })
            if shoeForm.is_valid():
                newShoe = Shoe.objects.create(name=shoeForm.cleaned_data['name'], owner=request.user)
                newShoe.save()

                return render(request, 'settings/shoe.html', {
                    'shoe': newShoe
                })
            else:
                return HttpResponseServerError()
        elif request.POST['todo'] == "deleteShoe":
            try:
                Shoe.objects.get(id=int(request.POST['shoeID'])).delete()
            except:
                return HttpResponseNotFound()

            return HttpResponse("")
        elif request.POST['todo'] == "updateAccountSettings":
            accountSettingsForm = AccountSettingsForm({
                'emailAddress'      :   request.POST['emailAddress'],
                'privacySelection'  :   request.POST['privacySelection'],
                'displayName'       :   request.POST['displayName'],
                'pdfName'           :   request.POST['pdfName']
            })
            if accountSettingsForm.is_valid():
                if authenticate(username=request.user.username, password=request.POST['password']) != None:
                    print("privacy received", accountSettingsForm.cleaned_data['privacySelection'])
                    if accountSettingsForm.cleaned_data['emailAddress'] != "":
                        request.user.email = accountSettingsForm.cleaned_data['emailAddress']
                    if accountSettingsForm.cleaned_data['privacySelection'] != 0:
                        request.user.userinfo.privacySelection = accountSettingsForm.cleaned_data['privacySelection']
                    if accountSettingsForm.cleaned_data['displayName'] != "":
                        request.user.userinfo.displayName = accountSettingsForm.cleaned_data['displayName']
                    if accountSettingsForm.cleaned_data['pdfName'] != "":
                        request.user.userinfo.pdfName = accountSettingsForm.cleaned_data['pdfName']
                    request.user.save()
                    request.user.userinfo.save()
                    return HttpResponse("")
                else:
                    return HttpResponseForbidden("The password you entered is invalid.")
            else:
                return HttpResponseBadRequest("The information you entered is invalid.")
        elif request.POST['todo'] == "addType":
            typeName = request.POST['newTypeName']
            workoutType = WorkoutType.objects.create(name=typeName, owner=request.user)
            workoutType.save()
            return render(request, "settings/type.html", { 'workoutType': workoutType })
        elif request.POST['todo'] == "deleteType":
            WorkoutType.objects.get(id=request.POST['typeID'], owner=request.user).delete()
            return HttpResponse()
        else:
            return HttpResponseBadRequest("This command isn't recognized.")







    if request.user.is_authenticated:
        if request.is_ajax():
            return settingsAJAX(request)

        templateDict = {}
        templateDict.update(localizationDict[baseLocale])
        templateDict.update({
            'shoes':    Shoe.objects.filter(owner=request.user)
        })
        return render(request, "settings/settings.html", templateDict)
    else:
        return HttpResponseRedirect(reverse("loginView"))


def importView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginView"))

    if request.method == "POST":
        form = ImportForm({
            'mervData': request.POST['mervData']
        })
        if form.is_valid():
            wdate          = r'(\d\d\d\d-\d{1,2}-\d{1,2}),'
            wtype         = r'(?<!")"(.*)"(?!"),'
            subtype       = r'(?<!")"(.*)"(?!"),'
            distance      = r'(?<!")"(\d*(?:\.\d+)?)"(?!"),'
            distanceUnits = r'(?<!")"(.*)"(?!"),'
            pace          = r'(?<!")"(\d*(?:\.\d+)?)"(?!"),'
            paceUnits     = r'(?<!")"(.*)"(?!"),'
            minutes       = r'(?<!")"(\d*(?:\.\d+)?)"(?!"),'
            shoe          = r'(?<!")"(.*)"(?!"),'
            heartrate     = r'(?<!")"(\d*(?:\.\d+)?)"(?!"),'
            title         = r'(?<!")"(.*)"(?!"),'
            addendum      = r'(?<!")"(.*)"(?!"),'
            entryText     = r'(?<!")"(.*)"(?!"),'


            regexPattern = wdate + wtype + subtype + distance + distanceUnits + pace + paceUnits + minutes + shoe + heartrate + title + addendum + entryText
            regexedWorkouts = re.findall(regexPattern, form.cleaned_data['mervData'])

            for workoutTuple in regexedWorkouts:
                workoutDate = workoutTuple[0].split('-')
                workoutType = None
                if WorkoutType.objects.filter(name=workoutTuple[1], owner=request.user).exists():
                    workoutType = WorkoutType.objects.get(name=workoutTuple[1], owner=request.user)
                elif WorkoutType.objects.filter(name=workoutTuple[1], owner__isnull=True).exists():
                    workoutType = WorkoutType.objects.get(name=workoutTuple[1], owner__isnull=True)
                else:
                    workoutType = WorkoutType.objects.create(name=workoutTuple[1], owner=request.user)
                    workoutType.save()

                shoe = None
                if Shoe.objects.filter(name=workoutTuple[8], owner=request.user).exists():
                    shoe = Shoe.objects.get(name=workoutTuple[8], owner=request.user)
                else:
                    shoe = Shoe.objects.create(name=workoutTuple[8], owner=request.user)
                    shoe.save()

                Workout.objects.create(
                    owner                   = request.user,
                    date                    = datetime.date(int(workoutDate[0]), int(workoutDate[1]), int(workoutDate[2])),
                    wtype                   = workoutType,
                    mervLegacySubtype       = workoutTuple[2],
                    distance                = (float(workoutTuple[3])*1.609 if workoutTuple[4] == 'km' else (float(workoutTuple[3]*1609 if workoutTuple[4] == 'm' else float(workoutTuple[3])))),
                    mervLegacyDistance      = float(workoutTuple[3]),
                    mervLegacyDistanceUnits = workoutTuple[4],
                    mervLegacyPace          = workoutTuple[5],
                    mervLegacyPaceUnits     = workoutTuple[6],
                    hours                   = int(float(workoutTuple[7])) // 60,
                    minutes                 = int(float(workoutTuple[7])) % 60,
                    seconds                 = round(60 * (float(workoutTuple[7]) - int(float(workoutTuple[7]))), 2),
                    shoe                    = shoe,
                    mervLegacyHeartrate     = int(workoutTuple[9]),
                    title                   = workoutTuple[10],
                    mervLegacyAddendum      = workoutTuple[11],
                    entry                   = workoutTuple[12].replace('""', '"'),
                    mervImport              = True,
                    modifiedDate            = datetime.datetime(1970, 1, 1, 0, 0, 0) # UNIX EPOCH TIME
                ).save()

            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, 'settings/import.html', baseLocalization[baseLocale])

    else:
        return render(request, 'settings/import.html', baseLocalization[baseLocale])
