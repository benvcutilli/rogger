from django.shortcuts import render
from shared.languageLocalization import baseLocalization

debugLocale = 'french'

entryFrenchDict = {
}
entryFrenchDict.update(baseLocalization['french'])

entryEnglishDict = {
}
entryEnglishDict.update(baseLocalization['english'])

entryLocalization = {
    'french'    :   entryFrenchDict,
    'english'   :   entryEnglishDict,
}

# Create your views here.

def newEntry(request):
    return render(request, "workoutLogging/newentry.html", entryLocalization[debugLocale])

def editEntry(request):
    return render(request, "workoutLogging/editentry.html", entryLocalization[debugLocale])

def viewEntry(request):
    return render(request, "workoutLogging/viewentry.html", entryLocalization[debugLocale])
