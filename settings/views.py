from django.shortcuts import render
from shared.languageLocalization import baseLocalization
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    if request.user.is_authenticated:

        return render(request, "settings/settings.html", localizationDict[baseLocale])
    else:
        return HttpResponseRedirect(reverse("loginView"))
