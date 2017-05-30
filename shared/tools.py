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

    def dayOfWeekWorded(self):
        daysDict = {
            1   :   "Monday",
            2   :   "Tuesday",
            3   :   "Wednesday",
            4   :   "Thursday",
            5   :   "Friday",
            6   :   "Saturday",
            7   :   "Sunday"
        }
        return daysDict[self.date.isoweekday()]

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle

class WorkoutWeek():
    def __init__(self, days, user=None):
        self.days = days
        self.user = user

    def getStats(self):
        workoutTypes = {}
        for day in self.days:
            for workout in day.workouts:
                if workout.wtype.name in workoutTypes:
                    workoutTypes[workout.wtype.name] += workout.distance
                else:
                    workoutTypes[workout.wtype.name] = workout.distance

        return [key + ": " + str(workoutTypes[key]) for key in workoutTypes]

    def getPDF(self, responseObject):
        pdf = SimpleDocTemplate(responseObject, pagesize=letter)
        flowables = []
        dateStyle = ParagraphStyle("")
        dateStyle.spaceBefore           = 12
        dateStyle.spaceAfter            = 12
        dateStyle.fontSize              = 16
        dateStyle.fontName              = "Times-Roman"
        workoutInfoStyle                = ParagraphStyle("")
        workoutInfoStyle.fontName       = "Times-Roman"
        workoutInfoStyle.spaceBefore    = 8
        workoutEntryStyle               = ParagraphStyle("")
        workoutEntryStyle.spaceBefore   = 4
        workoutEntryStyle.fontName      = "Times-Roman"
        flowables.append(Paragraph(self.user.userinfo.pdfName, dateStyle))
        flowables.append(Paragraph("", dateStyle))
        for day in self.days:
            flowables.append(Paragraph(str(day.date.strftime("%A, %B %d, %Y")), dateStyle))
            for workout in day.workouts:
                flowables.append(Paragraph("<strong>" + workout.title + " - " + str(workout.distance) + " miles" + (" - " + workout.wtype.name if workout.wtype != None else "") + (" - " + workout.shoe.name if workout.shoe != None else "") + "</strong>", workoutInfoStyle))
                # using <br/>'s from citation [24]
                flowables.append(Paragraph(workout.entry.replace("\r\n", "<br/>"), workoutEntryStyle))

        weekTotalStyle  = dateStyle
        statStyle       = workoutEntryStyle

        flowables.append(Paragraph("Week Totals", weekTotalStyle))
        for stat in self.getStats():
            flowables.append(Paragraph(stat, statStyle))

        pdf.build(flowables)

def getWeek(year, month, day, user):
    currentDate = date(year, month, day)
    days = []
    for i in range(7):
        days.append(WorkoutDay(currentDate, Workout.objects.filter(owner=user, date=currentDate)))
        currentDate += timedelta(1)

    return WorkoutWeek(days, user)

def getWeeksForMonthRepresentation(monthNumber, yearNumber, user):
    day = date(yearNumber, monthNumber, 1)
    dayList = []
    while day.month == monthNumber:
        dayList.append(WorkoutDay(day, Workout.objects.filter(date=day, owner=user)))
        day += timedelta(1)

    backwards   =   dayList[0].date.isoweekday() - 1
    forwards    =   7 - dayList[-1].date.isoweekday()

    day = dayList[0].date
    for i in range(backwards):
        day -= timedelta(1)
        dayList.insert(0, WorkoutDay(day, Workout.objects.filter(date=day, owner=user)))

    day = dayList[-1].date
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
    def monthWorded(self):
        monthDict = {
            1   :   "January",
            2   :   "February",
            3   :   "March",
            4   :   "April",
            5   :   "May",
            6   :   "June",
            7   :   "July",
            8   :   "August",
            9   :   "September",
            10  :   "October",
            11  :   "November",
            12  :   "December"
        }

        return monthDict[self.month]

def getSurroundingMonths(monthNumber, yearNumber, user, before=5, after=6):
    monthsWeeks = [WorkoutMonth(getWeeksForMonthRepresentation(monthNumber, yearNumber, user), monthNumber, yearNumber)]
    tempYearNumber      =   yearNumber
    tempMonthNumber     =   monthNumber
    for i in range(before):
        # citation [19]
        tempMonthNumber -= 1
        if tempMonthNumber < 1:
            tempMonthNumber =   12
            tempYearNumber  -=  1
        # end citation
        monthsWeeks.insert(0, WorkoutMonth(getWeeksForMonthRepresentation(tempMonthNumber, tempYearNumber, user), tempMonthNumber, tempYearNumber))

    tempYearNumber      =   yearNumber
    tempMonthNumber     =   monthNumber
    for i in range(after):
        # citation [19]
        tempMonthNumber += 1
        if tempMonthNumber > 12:
            tempMonthNumber =   1
            tempYearNumber  +=  1
        # end citation
        monthsWeeks.append(WorkoutMonth(getWeeksForMonthRepresentation(tempMonthNumber, tempYearNumber, user), tempMonthNumber, tempYearNumber))




    return monthsWeeks
