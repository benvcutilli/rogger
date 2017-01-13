from django.shortcuts import render
from shared.languageLocalization import baseLocalization, debugLocale
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from shared.tools import getSurroundingMonths
from datetime import date
# Create your views here.

######### USER PAGE LOCALIZATION #############
userPageFrenchDict = {

}
userPageFrenchDict.update(baseLocalization['french'])

userPageEnglishDict = {

}
userPageEnglishDict.update(baseLocalization['english'])

userPageLocalization = {
    'french' : userPageFrenchDict,
    'english': userPageEnglishDict,
}
######## END LOCALIZATION ####################

def userView(request, username):
    templateDict = {}
    templateDict.update(userPageLocalization[debugLocale])
    if not User.objects.filter(username=username).exists():
        return HttpResponseNotFound()
    else:
        user = User.objects.get(username=username)
        if user.userinfo.privacySelection == 2 and request.user != user:
            return HttpResponseNotFound()
        else:
            months = getSurroundingMonths(date.today().month, date.today().year, user)
            print(months)
            templateDict.update({
                'months': months
            })

    return render(request, 'userProfile/userProfileBase.html', templateDict)
