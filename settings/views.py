from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse
from settings.forms import ShoeForm
from settings.models import Shoe

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
        shoeForm = ShoeForm({
            'name'  :   request.POST['newShoeName'],
        })
        if shoeForm.is_valid():
            newShoe = Shoe.objects.create(name=shoeForm.cleaned_data['name'], userInfo=request.user.userinfo)
            newShoe.save()

            return render(request, 'settings/shoe.html', {
                'shoe': newShoe
            })
        else:
            return HttpResponseServerError()

    if request.user.is_authenticated:
        if request.is_ajax():
            return settingsAJAX(request)

        templateDict = {}
        templateDict.update(localizationDict[baseLocale])
        templateDict.update({
            'shoes':    Shoe.objects.filter(userInfo=request.user.userinfo)
        })
        return render(request, "settings/settings.html", templateDict)
    else:
        return HttpResponseRedirect(reverse("loginView"))
