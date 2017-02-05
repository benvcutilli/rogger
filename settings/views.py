from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.urls import reverse
from settings.forms import ShoeForm, AccountSettingsForm
from settings.models import Shoe, WorkoutType
from django.contrib.auth import authenticate

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
                return HttpResponseServerError()

            return HttpResponse("")
        elif request.POST['todo'] == "updateAccountSettings":
            accountSettingsForm = AccountSettingsForm({
                'emailAddress'      :   request.POST['emailAddress'],
                'privacySelection'  :   request.POST['privacySelection'],
                'displayName'       :   request.POST['displayName'],
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
