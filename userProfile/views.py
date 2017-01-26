from django.shortcuts import render
from shared.languageLocalization import baseLocalization, debugLocale
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from shared.tools import getSurroundingMonths, getWeek
from shared.models import Follow, Block
from datetime import date
from workoutLogging.models import Workout
from django.template.loader import render_to_string
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
        if (user.userinfo.privacySelection == 3 and request.user != user) or (Block.objects.filter(blockee=request.user, blocker=user).exists()):
            return HttpResponseNotFound()
        else:
            if request.is_ajax():
                return userViewAJAX(request, username)


            months = getSurroundingMonths(date.today().month, date.today().year, user)

            templateDict.update({
                'months'        :   months,
                'earliestMonth' :   months[0].month,
                'earliestYear'  :   months[0].year,
                'latestMonth'   :   months[-1].month,
                'latestYear'    :   months[-1].year,
                'profileOwner'  :   user,
                'mileage'       :   sum([workout.distance for workout in Workout.objects.filter(owner=user)]),
                'followsUser'   :   Follow.objects.filter(followee=user, follower=request.user).exists() if request.user.is_authenticated else None,
                'blocked'       :   Block.objects.filter(blockee=user, blocker=request.user) if request.user.is_authenticated else None
            })

    return render(request, 'userProfile/userProfileBase.html', templateDict)


def userViewAJAX(request, username):
    if not User.objects.filter(username=username).exists():
        return HttpResponseNotFound()
    else:
        user = User.objects.get(username=username)
        if (user.userinfo.privacySelection >= 2 and user != request.user):
            return HttpResponseForbidden()
        else if (Block.objects.filter(blockee=request.user, blocker=user).exists() and request.user != user):
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
            elif request.POST['todo']   ==  "updateCalendar":
                months = getSurroundingMonths(int(request.POST['month']), int(request.POST['year']), user)
                return JsonResponse({
                    'earlierMonth'  :   months[0].month,
                    'earlierYear'   :   months[0].year,
                    'laterMonth'    :   months[-1].month,
                    'laterYear'     :   months[-1].year,
                    'html'          :   render_to_string("userProfile/months.html", { 'months': months, 'profileOwner': user, 'user': request.user })
                })
            elif request.POST['todo']   ==  "scrollEarlier":
                months = getSurroundingMonths(int(request.POST['month']), int(request.POST['year']), user, 12, 0)[:-1]
                return JsonResponse({
                    'month' :   months[0].month,
                    'year'  :   months[0].year,
                    'html'          :   render_to_string("userProfile/months.html", { 'months': months, 'profileOwner': user, 'user': request.user })
                })
            elif request.POST['todo']   ==  "scrollLater":
                months = getSurroundingMonths(int(request.POST['month']), int(request.POST['year']), user, 0, 12)[1:]
                return JsonResponse({
                    'month' :   months[-1].month,
                    'year'  :   months[-1].year,
                    'html'          :   render_to_string("userProfile/months.html", { 'months': months, 'profileOwner': user, 'user': request.user })
                })
            elif request.POST['todo']   ==  "blockAction":
                if request.user.is_authenticated():
                    if not Block.objects.filter(blockee=user, blocker=request.user).exists() and user != request.user:
                        Block.objects.create(blockee=user, blocker=request.user).save()
                        return HttpResponse("1")
                    else:
                        Block.objects.get(blockee=user, blocker=request.user).delete()
                        return HttpResponse("0")
                else:
                    return HttpResponseBadRequest("You need to be logged in to use this function")
            else:
                return HttpResponseBadRequest()


def weekPDFView(request, username, yearString, monthString, dayString):
    year    =   int(yearString)
    month   =   int(monthString)
    day     =   int(dayString)

    if User.objects.get(username=username).userinfo.privacySelection == 3 and request.user.username != username:
        return HttpResponseNotFound()
    if not (request.user.is_authenticated and request.user.username == username):
        return HttpResponseForbidden()

    pdfResponse = HttpResponse(content_type="application/pdf")
    pdfResponse['Content-Disposition'] = 'attachment; filename=week' + yearString + "." + monthString + "." + dayString + ".pdf"
    getWeek(year, month, day, request.user).getPDF(pdfResponse)
    return pdfResponse
