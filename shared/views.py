from django.shortcuts import render
from collections import Counter
from django.contrib.auth.models import User
from shared.models import Follow, Block
from shared.languageLocalization import debugLocale, baseLocalization

possibleBigrams = []
for c1 in "abcdefghijklmnopqrstuvwxyz_ ":
    for c2 in "abcdefghijklmnopqrstuvwxyz_ ":
        possibleBigrams.append(c1 + c2)



class Histogram():
    def __init__(self, phrase):
        self.phrase = phrase.lower()
        global possibleBigrams
        histo = Counter(possibleBigrams)
        for c in range(len(self.phrase) - 1):
            if self.phrase[c:c+2] in histo:
                histo[self.phrase[c:c+2]] += 1
        histo = list(histo.items())
        histo.sort(key=lambda item: item[0])
        self.histo  = [ thing[1] for thing in histo ]

    def distance(self, other):
        otherHistogram = Histogram(other)
        distance = 0
        for i in range(len(self.histo)):
            distance += (self.histo[i] - otherHistogram.histo[i])**2

        return distance

def search(request):
    users = User.objects.all()
    searchPhrase = request.POST['searchphrase']
    results = []
    for user in users:
        block   = Block.objects.filter(blocker=request.user, blockee=user).exists() or Block.objects.filter(blockee=request.user, blocker=user).exists()
        follow  = Follow.objects.filter(follower=request.user, followee=user).exists()

        if not user.is_staff and ((user.userinfo.privacySelection == 1 and not block) or (user.userinfo.privacySelection == 2 and follow and not block)):
            if user.userinfo.searchUsername and user.userinfo.searchDisplayName:
                results.append((user, min(Histogram(user.username).distance(searchPhrase), Histogram(user.userinfo.displayName).distance(searchPhrase))))
            elif user.userinfo.searchUsername:
                results.append((user, Histogram(user.username).distance(searchPhrase)))
            elif user.userinfo.searchDisplayName:
                results.append((user, Histogram(user.userinfo.displayName).distance(searchPhrase)))

    results.sort(key=(lambda pair: pair[1]))
    #results.reverse()
    return render(request, "shared/searchmatches.html", { 'matches' : [u[0] for u in results] })



def error400View(request):
    return render(request, 'shared/templates/error400.html', baseLocalization[debugLocale])
def error403View(request):
    return render(request, 'shared/templates/error403.html', baseLocalization[debugLocale])
def error404View(request):
    return render(request, 'shared/templates/error404.html', baseLocalization[debugLocale])
def error500View(request):
    return render(request, 'shared/templates/error500.html', baseLocalization[debugLocale])
