from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage(request):
    if not request.user.is_authenticated:
        return loginView(request)
    else:
        return render(request, 'homepage/homepage.html', {})


def loginView(request):
    return render(request, 'homepage/login.html', {})
