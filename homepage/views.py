from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from shared.languageLocalization import baseLocalization
from rogger.settings import RECAPTCHA_PUBLIC, RECAPTCHA_SECRET
from . import forms
import urllib
import json
from django.contrib.auth.models import User

debugLocale = 'french'
godMode = True

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

######### END OF LOCALIZATION ##########
def homepage(request):
    if not request.user.is_authenticated and not godMode:
        return loginView(request)
    else:
        return render(request, 'homepage/homepage.html', homepageLocalization[debugLocale])


def loginView(request):



    if request.method == "POST":
        return HttpResponseRedirect(reverse("homepage"))
    else:
        return render(request, 'homepage/login.html', loginLocalization[debugLocale])


def newAccountView(request):
    templateDict = createAccountLocalizationDict[debugLocale]
    templateDict.update({
        "error" : ""
    })
    templateDict.update({
        'recaptchaPublic': RECAPTCHA_PUBLIC,
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

            if not creationForm.cleaned_data['password'] == creationForm.cleaned_data['passwordConfirmation']:
                error = "Your passwords don't match"

            if User.objects.filter(username=creationForm.cleaned_data['username']).exists():
                error = "That username is already in use :("



            if error != "":
                templateDict['error'] = error
                print(templateDict['error'])
                return render(request, 'homepage/newaccount.html', templateDict)
            else:
                User.objects.create_user(creationForm.cleaned_data['username'], creationForm.cleaned_data['emailAddress'], creationForm['password']).save()
                return HttpResponseRedirect(reverse("homepage"))





        else:
            errorString = ""
            formTranslation = {
                'passwordConfirmation'  :   "password confirmation",
                'password'              :   "password",
                'username'              :   "username",
                'emailAddress'          :   "email address"
            }
            for key in creationForm.errors:
                errorString += formTranslation[key] + ": " + ", ".join([creationForm.errors[key][i] for i in range(len(creationForm.errors[key]))]) + '\n'
            templateDict.update({
                'error': errorString,
            })

            return render(request, 'homepage/newaccount.html', templateDict)


    # NOT A FORM
    else:
        return render(request, 'homepage/newaccount.html', templateDict)
