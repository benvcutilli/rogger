def getErrorString(form):
    errorString = ""
    for key in creationForm.errors:
        errorString += form.formTranslation[key] + ": " + ", ".join([creationForm.errors[key][i] for i in range(len(creationForm.errors[key]))])

    return errorString


from settings.models import WorkoutType, universalWorkoutTypeNames

def initializeUniversalTypes():
    for workoutType in universalWorkoutTypeNames:
        WorkoutType.objects.create(owner=None, name=workoutType[0], displayMeasurement=workoutType[1]).save()

from datetime import date, timedelta

def getWeeksForMonthRepresentation(monthNumber, yearNumber):
    day = date(yearNumber, monthNumber, 1)
    dayList = []
    while day.month == monthNumber:
        dayList.append(day)
        day += timedelta(1)

    backwards   =   dayList[0].isoweekday() - 1
    forwards    =   7 - dayList[-1].isoweekday()

    day = dayList[0]
    for i in range(backwards):
        day -= timedelta(1)
        dayList.insert(0, day)

    day = dayList[-1]
    for i in range(forwards):
        day += timedelta(1)
        dayList.append(day)

    weekList = []
    for i in range(len(dayList)//7):
        weekList.append(dayList[i*7:(i+1)*7])

    return weekList
