def getErrorString(form):
    errorString = ""
    for key in creationForm.errors:
        errorString += form.formTranslation[key] + ": " + ", ".join([creationForm.errors[key][i] for i in range(len(creationForm.errors[key]))])

    return errorString


from settings.models import WorkoutType, universalWorkoutTypeNames

def initializeUniversalTypes():
    for workoutType in universalWorkoutTypeNames:
        WorkoutType.objects.create(owner=None, name=workoutType[0], displayMeasurement=workoutType[1]).save()
