# File probably auto-generated by Django [95], maybe django-admin startapp
# [79, "startapp" documentation].

# [79, "startproject" documentation] may have included the following import
# line in this file at file creation time.
from django.shortcuts import render
from shared.languageLocalization import baseLocalization, debugLocale
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from shared.tools import getSurroundingMonths, getWeek, cropProfilePicture
from shared.models import Follow, Block
from datetime import date
from workoutLogging.models import Workout
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
# No longer used (this is the "boto3" package[195])
# import boto3
from decimal import Decimal


# A. This code is code that handled saving the images to S3[77]; S3 usage is no longer the case, so
#    this is merely commented out

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
        user = get_object_or_404(User, username=username)
        if (user.userinfo.privacySelection == 3 and request.user != user) or (request.user.is_authenticated and Block.objects.filter(blockee=request.user, blocker=user).exists() and request.user != user):
            return HttpResponseNotFound()

        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return userViewAJAX(request, username)

            # usage of the "approved" attribute in a Follow object from citation [25]
            if user.userinfo.privacySelection == 2 and ((request.user.is_authenticated and not Follow.objects.filter(followee=user, follower=request.user, approved=True).exists()) or not request.user.is_authenticated) and request.user != user:
                templateDict.update({
                    'profileOwner'  :   user,
                    # [107] provides the rationale for including this "mileage" key-value entry:
                    'mileage'       :   Decimal(str(sum([workout.distance for workout in Workout.objects.filter(owner=user)]))).normalize(),
                    'followsUser'   :   Follow.objects.filter(followee=user, follower=request.user).exists() if request.user.is_authenticated else None,
                    'blocked'       :   Block.objects.filter(blockee=user, blocker=request.user) if request.user.is_authenticated else None
                })
                return render(request, "userProfile/userProfilePrivate.html", templateDict)

            # The data that will be used to fill in the calendar which functions
            # according to [69]
            months = getSurroundingMonths(date.today().month, date.today().year, user)

            templateDict.update({
                # The variables passed to the Django template [109], which are
                # used to support the functionality described in [69]
                ################################################################
                #                                                              #

                'months'        :   months,
                'earliestMonth' :   months[0].month,
                'earliestYear'  :   months[0].year,
                'latestMonth'   :   months[-1].month,
                'latestYear'    :   months[-1].year,
                'profileOwner'  :   user,

                #                                                              #
                ################################################################
                # [107] provides the rationale for including this "mileage" key-value entry:
                'mileage'       :   Decimal(str(sum([workout.distance for workout in Workout.objects.filter(owner=user)]))),
                'followsUser'   :   Follow.objects.filter(followee=user, follower=request.user).exists() if request.user.is_authenticated else None,
                'blocked'       :   Block.objects.filter(blockee=user, blocker=request.user) if request.user.is_authenticated else None
            })

    return render(request, 'userProfile/userProfileBase.html', templateDict)


def userViewAJAX(request, username):
    if not User.objects.filter(username=username).exists():
        return HttpResponseNotFound()
    else:
        user = get_object_or_404(User, username=username)
        if   request.POST['todo']   ==  "followAction":
            if request.user.is_authenticated:
                if not Follow.objects.filter(followee=user, follower=request.user).exists():
                    if user == request.user:
                        # usage of the "approved" attribute in a Follow object from citation [25]
                        Follow.objects.create(followee=user, follower=request.user, approved=True).save()
                    else:
                        Follow.objects.create(followee=user, follower=request.user).save()
                    return HttpResponse("1")
                else:
                    Follow.objects.get(followee=user, follower=request.user).delete()
                    return HttpResponse("0")
            else:
                return HttpResponseBadRequest("You need to be logged in to use this function")
        elif request.POST['todo']   ==  "updateCalendar":
            # usage of the "approved" attribute in a Follow object from citation [25]
            if user.userinfo.privacySelection == 2 and not Follow.objects.filter(followee=user, follower=request.user, approved=True).exists():
                return HttpResponseForbidden()

            # "months" is used to fill in [69]'s calendar
            months = getSurroundingMonths(int(request.POST['month']), int(request.POST['year']), user)
            return JsonResponse({

                # Sending updated values for the Javascript variables used to
                # control the calendar in the manner of [60]
                ################################################################
                #                                                              #

                'earlierMonth'  :   months[0].month,
                'earlierYear'   :   months[0].year,
                'laterMonth'    :   months[-1].month,
                'laterYear'     :   months[-1].year,

                #                                                              #
                ################################################################
                'html'          :   render_to_string("userProfile/months.html", { 'months': months, 'profileOwner': user, 'user': request.user })
            })
        # The case where we are fetching calendar information from before the
        # earliest time shown on the calendar (see [69] for why this
        # functionality exists):
        elif request.POST['todo']   ==  "scrollEarlier":
            # usage of the "approved" attribute in a Follow object from citation [25]
            if user.userinfo.privacySelection == 2 and not Follow.objects.filter(followee=user, follower=request.user, approved=True).exists():
                return HttpResponseForbidden()
            months = getSurroundingMonths(int(request.POST['month']), int(request.POST['year']), user, 12, 0)[:-1]
            return JsonResponse({
                'month' :   months[0].month,
                'year'  :   months[0].year,
                'html'  :   render_to_string("userProfile/months.html", { 'months': months, 'profileOwner': user, 'user': request.user })
            })
        # The case described in [69] where we get newer calendar data:
        elif request.POST['todo']   ==  "scrollLater":
            # usage of the "approved" attribute in a Follow object from citation [25]
            if user.userinfo.privacySelection == 2 and not Follow.objects.filter(followee=user, follower=request.user, approved=True).exists():
                return HttpResponseForbidden()
            months = getSurroundingMonths(int(request.POST['month']), int(request.POST['year']), user, 0, 12)[1:]
            return JsonResponse({
                'month' :   months[-1].month,
                'year'  :   months[-1].year,
                'html'  :   render_to_string("userProfile/months.html", { 'months': months, 'profileOwner': user, 'user': request.user })
            })
        elif request.POST['todo']   ==  "blockAction":
            if request.user.is_authenticated:
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

# The function used to create a PDF with the week's workouts, an idea from [110]
def weekPDFView(request, username, yearString, monthString, dayString):
    year    =   int(yearString)
    month   =   int(monthString)
    day     =   int(dayString)

    user = get_object_or_404(User, username=username)
    if (user.userinfo.privacySelection == 3 and request.user != user) or (request.user.is_authenticated and Block.objects.filter(blockee=user, blocker=request.user).exists() and request.user != user):
        return HttpResponseNotFound()
    if not (request.user.is_authenticated and request.user.username == username):
        return HttpResponseForbidden()

    # Value for content_type is from [111] and refers to [74, 14.17]
    pdfResponse = HttpResponse(content_type="application/pdf")
    # [111] provided the key used in this dictionary-setting and possibly
    # reference [111] provided the text (with the exception of what "filename"
    # is set to) used in the string that we set to this key
    pdfResponse['Content-Disposition'] = 'attachment; filename=week' + yearString + "." + monthString + "." + dayString + ".pdf"
    getWeek(year, month, day, request.user).getPDF(pdfResponse)
    return pdfResponse


# This technique (used in the function storeDate below) of storing the date (for
# a new log entry) in the user's Django session [112] is from citation [25]
def storeDate(request):
    if not user.is_authenticated:
        return HttpReponseForbidden()

    if request.POST.has_key('entryDate'):
        request.session['newWorkoutDate'] = request.POST['entryDate']
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


from rogger.settings import MEDIA_BUCKET_NAME, MEDIA_BUCKET_ID, MEDIA_BUCKET_SECRET, PICTURE_STORE
from io import BytesIO

# CITATION [26]
def changePictureView(request, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.method == "POST":

            # Need to possibly delete their profile picture, which is likely a requirement described
            # in [255]
            ########################################################################################
            #                                                                                      #

            if request.user.userinfo.uploadedProfilePicture and "deletePicture" in request.POST:
                path = request.user.userinfo.profilePicturePath()
                path.unlink()
                path = request.user.userinfo.thumbPath()
                path.unlink()

                request.user.userinfo.uploadedProfilePicture = False
                request.user.userinfo.save()

                parameters = {
                    "args": [request.user.username],
                    "viewname": "userView"
                }
                return HttpResponseRedirect(
                    reverse(**parameters)
                )

            #                                                                                      #
            ########################################################################################

            # Commented out because of (A)
            ######################################################################################################################################################################
            #                                                                                                                                                                    #

            # mediaBucket = boto3.resource('s3', aws_access_key_id=MEDIA_BUCKET_ID, aws_secret_access_key=MEDIA_BUCKET_SECRET).Bucket(MEDIA_BUCKET_NAME)
            # # This next line is to counter a bug where the profile picture will
            # # successfully be uploaded but the thumbnail will not be,
            # # potentially leading the user to believe that their old profile
            # # picture was completely erased from the system. See [113] for bug
            # # credits:
            # mediaBucket.delete_objects(Delete={"Objects": [{"Key": "profilepictureofuser"+str(request.user.id)}, {"Key": "thumbofuser"+str(request.user.id)}], "Quiet": True})

            #                                                                                                                                                                    #
            ######################################################################################################################################################################

            pictureFile = request.FILES['pictureFile']

            # This variable was used for the purposes described in point A
            # croppedPictureFile = BytesIO()

            # This section crops and stores the images on the machine in the encrypted device;
            # encryption is used because of the reasons outlined in "ENCRYPTION" of the README
            ###############################################################################################################
            #                                                                                                             #

            croppedPictureFile = PICTURE_STORE + "profilepictureofuser" + str(request.user.id) + ".png"
            cropProfilePicture(pictureFile, "full").save(croppedPictureFile, format='PNG')

            # Point A describes this section
            ###############################################################################################################
            #                                                                                                             #

            # # NEXT LINE POSSIBLY VERBATIM (with appropriate modification)
            # # FROM CITATION [36]
            # croppedPictureFile.seek(0)
            # mediaBucket.put_object(Key="profilepictureofuser" + str(request.user.id) + ".png", Body=croppedPictureFile)
            # croppedPictureFile = BytesIO()

            #                                                                                                             #
            ###############################################################################################################

            croppedPictureFile = PICTURE_STORE + "thumbofuser" + str(request.user.id) + ".png"
            cropProfilePicture(pictureFile, "thumb").save(croppedPictureFile, format='PNG')

            #                                                                                                             #
            ###############################################################################################################


            # Relevant comment: see A at top of file
            ###############################################################################################################
            #                                                                                                             #

            # # NEXT LINE POSSIBLY VERBATIM (with appropriate modification)
            # # FROM CITATION [36]
            # croppedPictureFile.seek(0)
            # mediaBucket.put_object(Key="thumbofuser" + str(request.user.id) + ".png", Body=croppedPictureFile)

            #                                                                                                             #
            ###############################################################################################################

            request.user.userinfo.uploadedProfilePicture = True
            request.user.userinfo.save()
            return HttpResponseRedirect(reverse('userView', args=[username]))
        else:
            return HttpResponseBadRequest()
    else:
        if User.objects.get(username=username).userinfo.privacySelection == 3:
            return HttpResponseNotFound()
        else:
            return HttpResponseForbidden()
# END CITATION
