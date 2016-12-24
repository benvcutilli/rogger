from django.shortcuts import render
from shared.languageLocalization import baseLocalization

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
    return render(request, "settings/settings.html", localizationDict[baseLocale])
