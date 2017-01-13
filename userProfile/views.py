from django.shortcuts import render
from shared.languageLocalization import baseLocalization, debugLocale
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.models import User
from shared.tools import getSurroundingMonths
from shared.models import Follow, Block
from datetime import date
from workoutLogging.models import Workout
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
            if request.is_ajax():
                return userViewAJAX(request, username)


            months = getSurroundingMonths(date.today().month, date.today().year, user)

            templateDict.update({
                'months'        :   months,
                'profileOwner'  :   user,
                'mileage'       :   sum([workout.distance for workout in Workout.objects.filter(owner=user)])
            })

    return render(request, 'userProfile/userProfileBase.html', templateDict)


def userViewAJAX(request, username):
    if not User.objects.filter(username=username).exists():
        return HttpResponseNotFound()
    else:
        user = User.objects.get(username=username)
        if (user.userinfo.privacySelection == 2 and user != request.user) or (Block.objects.filter(blockee=request.user, blocker=user).exists() and request.user != user):
            return HttpResponseNotFound()
        else:
            if   request.POST['todo']   ==  "followAction":
                if request.user.is_authenticated():
                    if not Follow.objects.filter(followee=user, follower=request.user).exists():
                        Follow.objects.create(followee=user, follower=request.user).save()
                        return HttpResponse("1")
                    else:
                        Follow.objects.get(followee=user, follower=request.user).delete()
                        return HttpResponse("0")
                else:
                    return HttpResponseBadRequest("You need to be logged in to use this function")
            elif request.POST['todo']   ==  "calendarChange":
                pass
            elif request.POST['todo']   ==  "blockaction":
                pass
            else:
                return HttpResponseBadRequest()
