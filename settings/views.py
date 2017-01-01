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
            newShoe = Shoe.objects.create(name=shoeForm.cleaned_data['name'])
            newShoe.save()

            return render(request, 'settings/shoe.html', {
                'name' : newShoe.name,
                'mileage': 0
            })
        else:
            return HttpResponseServerError()

    if request.user.is_authenticated:
        if request.is_ajax():
            return settingsAJAX(request)

        return render(request, "settings/settings.html", localizationDict[baseLocale])
    else:
        return HttpResponseRedirect(reverse("loginView"))
