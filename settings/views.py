# File probably auto-generated by Django [95], maybe django-admin startapp
# [79, "startapp" documentation].
#
# A. I have the parameter be called "request" just in case Django needs it to be (instead of
# something else). This view deletes a user (and all their corresponding data); see [244].
# Tried to pass in
#     login_url=reverse(
#        "loginView",
#        urlconf=rogger.urls
#    )
# to the decorator below. However, making rogger.urls available in this file causes an
# issue because rogger/urls.py does the same for this file (code like this was suggested to be
# the issue by an error message). So, it was removed and LOGIN_URL was set in the settings
# file instead.

# [79, "startproject" documentation] may have included the following import
# line in this file at file creation time.
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
from decimal import Decimal

import rogger.urls as t

# Documentation for this module: [239]
import random

# Function provided by [240]
import django.contrib.auth

# Importing [242]
import django.core.management

# Importing [245]
import django.core.mail

# The "Path" class found at [243, "Concrete paths"]
from pathlib import Path

# Importing [249]
import django.contrib.auth.decorators

from rogger import settings as configuration

from shared.models          import UserInfo, Block, Follow
from workoutLogging.models  import Comment, Workout, Unit
from settings.models        import Shoe, WorkoutType
from django.http import JsonResponse






baseLocale = 'english'

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
                # Checking the password for reasons discussed in [71]:
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
                    request.user.userinfo.searchUsername    = True if request.POST['searchUsername'] == "true" else False
                    request.user.userinfo.searchDisplayName = True if request.POST['searchDisplayName'] == "true" else False
                    request.user.save()
                    request.user.userinfo.save()
                    return HttpResponse("")
                else:
                    return HttpResponseForbidden("The password you entered is invalid.")
            else:
                return HttpResponseBadRequest("The information you entered is invalid.")
        elif request.POST['todo'] == "addType":
            typeName = request.POST['newTypeName']
            if WorkoutType.objects.filter(name=typeName, owner=request.user).exists():
                return HttpResponseBadRequest("A type of this name already exists.")
            workoutType = WorkoutType.objects.create(name=typeName, owner=request.user)
            workoutType.save()
            return render(request, "settings/type.html", { 'workoutType': workoutType })
        elif request.POST['todo'] == "deleteType":
            if WorkoutType.objects.get(id=request.POST['typeID'], owner=request.user).name != "Unknown":
                workoutType = WorkoutType.objects.get(id=request.POST['typeID'], owner=request.user)
                unknownWorkoutType = WorkoutType.objects.get(name="Unknown", owner=request.user)
                for workout in Workout.objects.filter(wtype=workoutType, owner=request.user):
                    workout.wtype       = unknownWorkoutType
                    workout.backupType  = workoutType.name
                    workout.save()
                workoutType.delete()
                return HttpResponse()
            else:
                return HttpResponseForbidden("You can't delete this type; this is a default type in case of deletion of other types.")
        elif request.POST['todo'] == "renameType":
            if WorkoutType.objects.get(id=request.POST['typeID'], owner=request.user).name != "Unknown":
                workoutType = WorkoutType.objects.get(id=request.POST['typeID'], owner=request.user)
                workoutType.name = request.POST['newName']
                workoutType.save()
                return HttpResponse()
            else:
                return HttpResponseForbidden("You can't delete this type; this is a default type in case of deletion of other types.")
        else:
            return HttpResponseBadRequest("This command isn't recognized.")







    if request.user.is_authenticated:
        if request.is_ajax():
            return settingsAJAX(request)

        templateDict = {}
        templateDict.update(localizationDict[baseLocale])
        templateDict.update({
            'shoes'         : Shoe.objects.filter(owner=request.user),
            'workoutTypes'  : WorkoutType.objects.filter(owner=request.user).exclude(name="Unknown")
        })
        return render(request, "settings/settings.html", templateDict)
    else:
        return HttpResponseRedirect(reverse("loginView"))

# This view imports data exported from Merv [70].
def importView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginView"))

    if request.method == "POST":
        form = ImportForm({
            'mervData': request.POST['mervData']
        })
        if form.is_valid():
            # Regular expressions capturing the information in a Merv export
            ####################################################################
            #                                                                  #

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

            #                                                                  #
            ####################################################################


            regexPattern = wdate + wtype + subtype + distance + distanceUnits + pace + paceUnits + minutes + shoe + heartrate + title + addendum + entryText
            regexedWorkouts = re.findall(regexPattern, form.cleaned_data['mervData'])

            for workoutTuple in regexedWorkouts:
                workoutDate = workoutTuple[0].split('-')
                workoutType = None
                if WorkoutType.objects.filter(name=workoutTuple[1], owner=request.user).exists():
                    workoutType = WorkoutType.objects.get(name=workoutTuple[2]+" "+workoutTuple[1], owner=request.user)
                else:
                    workoutType = WorkoutType.objects.create(name=workoutTuple[2]+" "+workoutTuple[1], owner=request.user)
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
                    mervOldRoggerLegacyType = workoutTuple[1],
                    mervLegacySubtype       = workoutTuple[2],
                    distance                = (Decimal(workoutTuple[3])*Decimal('1.609') if workoutTuple[4] == 'km' else (Decimal(workoutTuple[3])*Decimal('1609') if workoutTuple[4] == 'm' else Decimal(workoutTuple[3]))),
                    mervLegacyDistance      = Decimal(workoutTuple[3]),
                    mervLegacyDistanceUnits = workoutTuple[4],
                    mervLegacyPace          = workoutTuple[5],
                    mervLegacyPaceUnits     = workoutTuple[6],
                    hours                   = int(Decimal(workoutTuple[7])) // 60,
                    minutes                 = int(Decimal(workoutTuple[7])) % 60,
                    seconds                 = round(Decimal('60') * (Decimal(workoutTuple[7]) - int(Decimal(workoutTuple[7]))), 2),
                    shoe                    = shoe,
                    mervLegacyHeartrate     = int(workoutTuple[9]),
                    title                   = workoutTuple[10],
                    mervLegacyAddendum      = workoutTuple[11],
                    entry                   = workoutTuple[12].replace('""', '"'),
                    mervImport              = True,
                    modifiedDate            = datetime.datetime(1970, 1, 1, 0, 0, 0) # UNIX ([99]; that reference via [100, info box on right]) EPOCH TIME
                ).save()

            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, 'settings/import.html', baseLocalization[baseLocale])

    else:
        return render(request, 'settings/import.html', baseLocalization[baseLocale])
        
        







# Comment A is relevant for the next line and the function below it
@django.contrib.auth.decorators.login_required(   redirect_field_name=None   )
def datamanagement(request):

   
    
    def prepare(passwordError="", checkError=""):
        substitutions = {
            "toType":          "".join(   random.choices("cnposkew", k=6)   ),
            "passwordError":   passwordError,
            "checkError":      checkError,
            # Passed in so that we can show the user their pictures for download when they want
            # to exercise their GDPR rights[248] (GDPR can be found at [246])
            "user":            request.user
        }
        renderedTemplate = render(request, "settings/deletion.html", substitutions)
        return renderedTemplate





    # As is common, we use a conditional here to change the site's behavior for different kinds
    # of requests (specifically, their methods). [238] explains what else is going on here and 
    # associated references.
    if "GET" in request.method:
        response = prepare()
        return response

    elif "POST" in request.method:

        if request.POST["confirmation"] != request.POST["confirmationTruth"]:

            return prepare(checkError="You made a typo here")

        if not request.user.check_password(request.POST["accessProof"]):

            return prepare(passwordError="You entered the wrong password")

        else:
            
            primaryKey = request.user.pk 
            
            try:
                 
                profilePicture = Path(
                                    configuration.PICTURE_STORE,
                                    "{0}{1}.png".format(configuration.THUMBNAIL_PREFIX, primaryKey)
                                )
                thumbnail      = Path(
                                    configuration.PICTURE_STORE,
                                    "{0}{1}.png".format(
                                        configuration.PROFILE_PICTURE_PREFIX,
                                        primaryKey
                                    )
                                )
                thumbnail.unlink(True)
                profilePicture.unlink(True)
    
                deleting = request.user
                django.contrib.auth.logout(request)
                deleting.delete()
    
                django.core.management.call_command("clearsessions")
                
                page = render(request, "settings/deletioncompleted.html")
                return page

            except:
                
                # Making sure that the data is at least manually deleted
                django.core.mail.send_mail(
                    "Failure to delete account",
                    "Some data for account with primary key {0} couldn't be deleted. Please \
                        investigate and correct.".format(primaryKey),
                    "error@rogger.co",
                    [  "ben@rogger.co"  ]
                )
                
                page = render(request, "settings/deletionfailed.html")
                return page



# For important info, please take a look at A. Returns a JSONized chunk of data that the website
# had on the user (this is done because [248] says it needs to, although the exact format and system
# of data retrieval by the user, I think, isn't explicitly specified (for example, the data download
# probably doesn't need to happen right when the request is sent because other websites don't do
# that, I think).
@django.contrib.auth.decorators.login_required(   redirect_field_name=None   )
def export(request):
    
    data = {
        "Workout":      [ i for i in Workout.export(request.user) ],
        "Comment":      [ i for i in Comment.export(request.user) ],
        "Follow":       [ i for i in Follow.export(request.user) ],
        "Shoe":         [ i for i in Shoe.export(request.user) ],
        "WorkoutType":  [ i for i in WorkoutType.export(request.user) ],
        "Block":        [ i for i in Block.export(request.user) ],
        "UserInfo":     [ i for i in UserInfo.export(request.user) ],
        "Unit":         [ i for i in Unit.export(request.user) ]
    }
    
    jsonResponse = JsonResponse(data, json_dumps_params={ "indent": 7 })
    return jsonResponse
    
    
    