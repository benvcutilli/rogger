from django.shortcuts import render

# Create your views here.

def newEntry(request):
    return render(request, "workoutLogging/newentry.html", {})
