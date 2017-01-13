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
from workoutLogging.models import Workout

class WorkoutDay():
    def __init__(self, dateInstance, workouts):
        self.date = dateInstance
        self.workouts = workouts

class WorkoutWeek():
    def __init__(self, days):
        self.days = days

def getWeeksForMonthRepresentation(monthNumber, yearNumber, user):
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
        dayList.insert(0, WorkoutDay(day, Workout.objects.filter(date=day, owner=user)))

    day = dayList[-1]
    for i in range(forwards):
        day += timedelta(1)
        dayList.append(WorkoutDay(day, Workout.objects.filter(date=day, owner=user)))

    weekList = []
    for i in range(len(dayList)//7):
        weekList.append(WorkoutWeek(dayList[i*7:(i+1)*7]))

    return weekList


class WorkoutMonth():
    def __init__(self, weeks, month, year):
        self.weeks  = weeks
        self.month  = month
        self.year   = year

def getSurroundingMonths(monthNumber, yearNumber, user):
    monthsWeeks = [((monthNumber, yearNumber), getWeeksForMonthRepresentation(monthNumber, yearNumber, user))]
    tempYearNumber      =   yearNumber
    tempMonthNumber     =   monthNumber
    for i in range(5):
        # citation [19]
        tempMonthNumber -= 1
        if tempMonthNumber < 1:
            tempMonthNumber =   12
            tempYearNumber  -=  1
        # end citation
        monthsWeeks.insert(0, WorkoutMonth(getWeeksForMonthRepresentation(tempMonthNumber, tempYearNumber, user), tempMonthNumber, tempYearNumber))

    tempYearNumber      =   yearNumber
    tempMonthNumber     =   monthNumber
    for i in range(6):
        # citation [19]
        tempMonthNumber += 1
        if tempMonthNumber > 12:
            tempMonthNumber =   1
            tempYearNumber  +=  1
        # end citation
        monthsWeeks.append(WorkoutMonth(getWeeksForMonthRepresentation(tempMonthNumber, tempYearNumber, user), tempMonthNumber, tempYearNumber))




    return monthsWeeks
