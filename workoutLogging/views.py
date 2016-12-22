from django.shortcuts import render

# Create your views here.

def newEntry(request):
    return render(request, "workoutLogging/newentry.html", {})

def editEntry(request):
    return render(request, "workoutLogging/editentry.html", {})

def viewEntry(request):
    return render(request, "workoutLogging/viewentry.html", {})
