# File probably auto-generated by Django [95], maybe django-admin startapp
# [79, "startapp" documentation].

# [79, "startproject" documentation] may have included the following import
# line in this file at file creation time.
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.urls import reverse
from shared.languageLocalization import baseLocalization
from rogger.settings import RECAPTCHA_PUBLIC, RECAPTCHA_SECRET
from . import forms
import urllib
import json
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import password_reset_confirm, password_reset
from shared.tools import getErrorString
from django.contrib.auth.forms import SetPasswordForm
from shared.models import UserInfo, Follow, Block
from workoutLogging.models import Workout
from django.template.loader import render_to_string
from settings.models import WorkoutType

debugLocale = 'english'
godMode = False
forbiddenUsernames = ['rogger']

######### LOGIN LOCALIZATION ##########
loginFrenchDict = {
    'loginLocal': 'Connexion',
    'usernameLocal': 'nom d\'utiliser',
    'passwordLocal': 'mot de passe',
    'logInButtonLocal': 'Allons y!',
    'newUserLocal': 'Je n\'ai jamais été ici avant de ce moment',
    'forgotPasswordLocal': 'Alors...j\'ai oublié mon mot de passe',
}
loginFrenchDict.update(baseLocalization['french'])

loginEnglishDict = {
    'loginLocal': 'Login',
    'usernameLocal': 'username',
    'passwordLocal': 'password',
    'logInButtonLocal': 'Let\'s go!',
    'newUserLocal': 'I\'m new',
    'forgotPasswordLocal': 'Well...I forgot my password',
}
loginEnglishDict.update(baseLocalization['english'])

loginLocalization = {
    'french'    :   loginFrenchDict,
    'english'   :   loginEnglishDict,
}
######### END OF LOCALIZATION ##########

######### HOMEPAGE LOCALIZATION ########

homepageEnglishDict = {
    'updatesTitle'  :   'Updates',
    'followingTitle':   'Following',
    'noPosts'       :   'No posts :(',
    'encouragement' :   'Follow some people!',
    'updatedTag'    :   'updated'
}
homepageEnglishDict.update(baseLocalization['english'])

homepageFrenchDict = {
    'updatesTitle'  :   'Actualités',
    'followingTitle':   'Abonnements',
    'noPosts'       :   'Il n\'y a pas des actualités :(',
    'encouragement' :   'Abonnez-vous à des autres personnes!',
    'updatedTag'    :   'mis à jour'
}
homepageFrenchDict.update(baseLocalization['french'])

homepageLocalization = {
    'french'    :   homepageFrenchDict,
    'english'   :   homepageEnglishDict
}


createAccountFrenchDict = {

}
createAccountFrenchDict.update(baseLocalization['french'])

createAccountEnglishDict = {

}
createAccountEnglishDict.update(baseLocalization['english'])

createAccountLocalizationDict = {
    'french'    :   createAccountFrenchDict,
    'english'   :   createAccountEnglishDict,
}


changePasswordFrenchDict = {}
changePasswordFrenchDict.update(baseLocalization['french'])

changePasswordEnglishDict = {}
changePasswordEnglishDict.update(baseLocalization['english'])

changePasswordLocalizationDict = {
    'french'    :   changePasswordFrenchDict,
    'english'   :   changePasswordEnglishDict,
}

######### END OF LOCALIZATION ##########
def homepage(request):

    def homepageAJAX(request):
        if request.POST['todo'] == "fetchMoreUpdates":
            followedUsers = []
            for follow in Follow.objects.filter(follower=request.user):
                if not (Block.objects.filter(blocker=follow.followee, blockee=request.user).exists() or Block.objects.filter(blocker=request.user, blockee=follow.followee).exists() or (follow.followee.userinfo.privacySelection == 2 and follow.approved == False)): # usage of the "approved" attribute in a Follow object from citation [25]
                    followedUsers.append(follow.followee)
            workouts = Workout.objects.filter(owner__in=followedUsers) \
                                        .order_by("-modifiedDate", "id") \
                                        .filter(
                                            modifiedDate__lte=Workout.objects.get(id=int(request.POST['lastID'])).modifiedDate
                                        ).exclude(id=int(request.POST['lastID']))
            if not workouts.count() > 0:
                return HttpResponseNotFound()
            else:
                workouts = workouts[:(25 if workouts.count() >= 25 else len(workouts))]
                templateDict = {
                    'updates'   :   workouts,
                    'lastUpdateID':   workouts[len(workouts)-1].id if len(workouts) > 0 else -1
                }
                templateDict.update(homepageLocalization[debugLocale])
                return JsonResponse({
                    'id'    :   workouts[len(workouts)-1].id,
                    'html'  :   render_to_string("homepage/updates.html", templateDict)
                })

        if request.POST['todo'] == "acceptFollow":
            if request.user.userinfo.privacySelection < 2:
                return HttpResponseBadRequest("This action is only for users who have their profile locked")
            followID = request.POST['followID']
            follow = get_object_or_404(Follow, id=followID)
            # usage of the "approved" attribute in a Follow object from citation [25]
            follow.approved = True
            follow.save()
            return HttpResponse()
            # end citation
        else:
            return HttpResponseBadRequest()


    if not request.user.is_authenticated and not godMode:
        return loginView(request)
    else:
        if request.is_ajax():
            return homepageAJAX(request)

        followedUsers = []
        for follow in Follow.objects.filter(follower=request.user).order_by("followee__username"):
            if not (Block.objects.filter(blocker=follow.followee, blockee=request.user).exists() or Block.objects.filter(blocker=request.user, blockee=follow.followee).exists() or (follow.followee.userinfo.privacySelection == 2 and follow.approved == False) or follow.followee.userinfo.privacySelection == 3): # usage of the "approved" attribute in a Follow object from citation [25]
                followedUsers.append(follow.followee)
        workouts = Workout.objects.filter(owner__in=followedUsers).order_by("-modifiedDate", "id")
        templateDict = {
            'updates'           :   workouts[:workouts.count() if workouts.count() < 25 else 25],
            'lastUpdateID'        :   workouts[:workouts.count() if workouts.count() < 25 else 25][-1].id if len(workouts) > 0 else -1,
            #'earliestID':   workouts[workouts.count()-1 if workouts.count() < 25 else 24].id
            'follows'           :   followedUsers,
            # see citation [25] for where usage of "approved" in the next line comes from
            'followRequests'    :   Follow.objects.filter(followee=request.user, approved=False).exclude(follower__in=[ block.blockee for block in Block.objects.filter(blocker=request.user) ])
        }
        templateDict.update(homepageLocalization[debugLocale])

        return render(request, 'homepage/homepage.html', templateDict)












def loginView(request):

    templateDict = {}
    templateDict.update(loginLocalization[debugLocale])
    templateDict.update({
        'error' :   ""
    })

    if request.method == "POST":
        loginForm = forms.LoginForm({
            'username':   request.POST['username'],
            'password':   request.POST['password'],
        })

        if loginForm.is_valid():
            loggingInUser = authenticate(username=loginForm.cleaned_data['username'], password=loginForm.cleaned_data['password'])
            if loggingInUser != None:
                login(request, loggingInUser)
                return HttpResponseRedirect(reverse("homepage"))
            else:
                templateDict['error'] = "The username and/or password are incorrect :( Sorry (or maybe not sorry if you are a HACKER!)"
        else:
            templateDict['error'] = getErrorString(loginForm)

        return render(request, 'homepage/login.html', templateDict)
    else:
        return render(request, 'homepage/login.html', templateDict)













def newAccountView(request):
    templateDict = createAccountLocalizationDict[debugLocale]
    templateDict.update({
        "error" : ""
    })
    templateDict.update({
        'recaptchaPublic': RECAPTCHA_PUBLIC,
        'pageIsRecaptcha': "yes"
    })

    # IS A FORM
    if request.method == "POST":
        creationForm = forms.CreateAccountForm({
            'username'              : request.POST['username'],
            'password'              :   request.POST['password'],
            'passwordConfirmation'  :   request.POST['confirmPassword'],
            'emailAddress'          :   request.POST['emailAddress'],
        })

        if creationForm.is_valid():

            # This code handles bot protection provided by [53]. It's possible that some of this code is
            # copied from that site or from a subsite of that site; I can't remember, but just making sure
            # I cite it if necessary.
            ########################################################################################################
            #                                                                                                      #

            recaptchaResponse = request.POST['g-recaptcha-response']
            recaptchaRequest = urllib.request.Request(
                'https://www.google.com/recaptcha/api/siteverify',
                urllib.parse.urlencode({
                    'secret'    :   RECAPTCHA_SECRET,
                    'response'  :   recaptchaResponse,
                }).encode('ascii'),

            )

            recaptchaResult = json.loads(urllib.request.urlopen(recaptchaRequest).read().decode('ascii'))

            error = ""
            if not recaptchaResult['success'] == True:
                error = "Sorry, you seem to be a bot :( Please contact ben@rogger.co if you think this is a mistake"

            #                                                                                                      #
            ########################################################################################################

            if not creationForm.cleaned_data['password'] == creationForm.cleaned_data['passwordConfirmation']:
                error = "Your passwords don't match"

            global forbiddenUsernames
            if User.objects.filter(username=creationForm.cleaned_data['username']).exists() or creationForm.cleaned_data['username'] in forbiddenUsernames:
                error = "That username cannot be used :("

            for a in creationForm.cleaned_data["username"]:
                if a not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
                    error = "One or more of the characters in your username is not a number, underscore, or letter"



            if error != "":
                templateDict['error'] = error
                print(templateDict['error'])
                return render(request, 'homepage/newaccount.html', templateDict)
            else:
                newUser = User.objects.create_user(creationForm.cleaned_data['username'], creationForm.cleaned_data['emailAddress'], creationForm.cleaned_data['password'])
                newUser.save()
                UserInfo.objects.create(authUser=newUser).save()
                WorkoutType.objects.create(name="Unknown", owner=newUser)
                login(request, newUser)
                return HttpResponseRedirect(reverse("homepage"))





        else:
            templateDict.update({
                'error': getErrorString(creationForm, formTranslation),
            })

            return render(request, 'homepage/newaccount.html', templateDict)


    # NOT A FORM
    else:
        return render(request, 'homepage/newaccount.html', templateDict)


# This view allows a user to change a password, and the user needs to type their
# new password twice and their old password, which is common practice.
def changePasswordView(request):
    if request.user.is_authenticated:
        templateDict = {}
        templateDict.update({
            'error': ""
        })
        templateDict.update(changePasswordLocalizationDict[debugLocale])
        if request.method == "POST":
            changePasswordForm = forms.ChangePasswordForm({
                'newPassword'               :   request.POST['password'],
                'newPasswordConfirmation'   :   request.POST['confirmPassword'],
                'oldPassword'               :   request.POST['oldPassword']
            })
            if changePasswordForm.is_valid():
                if authenticate(username=request.user.username, password=changePasswordForm.cleaned_data['oldPassword']) != None:
                    if changePasswordForm.cleaned_data['newPassword'] == changePasswordForm.cleaned_data['newPasswordConfirmation']:
                        username = request.user.username
                        request.user.set_password(changePasswordForm.cleaned_data['newPassword'])
                        request.user.save()
                        login(request, User.objects.get(username=username))
                        return HttpResponseRedirect(reverse("homepage"))
                    else:
                        templateDict['error'] = "Your passwords don't match."
                else:
                    templateDict['error'] = "Your old password is incorrect"
            else:
                templateDict['error'] = getErrorString(changePasswordForm)

        return render(request, 'homepage/changepassword.html', templateDict)

    else:
        return HttpResponseRedirect(reverse("loginView"))

def passwordResetRequestView(request):
    return password_reset(request,
        template_name="homepage/resetpasswordrequest.html",
        email_template_name="homepage/passwordresetemail.txt",
        subject_template_name="homepage/passwordresetemailsubject.txt",
        post_reset_redirect=reverse("loginView"),
        from_email="reset@rogger.co"
    )

# The parameters that need to passed into this view may have been stated to be
# required by some webpage under the domain of [94]
def passwordResetView(request, uid, token):
    templateDict = {
        'uid'   :   uid,
        'token' :   token,
    }
    templateDict.update(baseLocalization[debugLocale])
    return password_reset_confirm(request,
        uidb64=uid,
        token=token,
        post_reset_redirect=reverse("loginView"),
        template_name='homepage/resetpassword.html',
        extra_context=templateDict,
        set_password_form=forms.RoggerSetPasswordForm
    )

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse("loginView"))
