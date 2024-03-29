def getErrorString(form):
    errorString = ""
    for key in form.errors:
        errorString += form.formTranslation[key] + ": " + ", ".join([form.errors[key][i] for i in range(len(form.errors[key]))])

    return errorString


from settings.models import WorkoutType
from workoutLogging.models import Unit
from decimal import Decimal
from shared.templatetags.sharedfilters import prettydecimal
from django.core.mail import send_mail
import time
from django.contrib.auth.models import User

def initializeUniversals():
    units = {
        'miles':      Decimal('1.0'),
        'mile':       Decimal('1.0'),
        'mi':         Decimal('1.0'),
        'meters':     Decimal('1.0')/Decimal('1609.0'),
        'meter':      Decimal('1.0')/Decimal('1609.0'),
        'm':          Decimal('1.0')/Decimal('1609.0'),
        'kilometers': Decimal('1.0')/Decimal('1.609'),
        'kilometer':  Decimal('1.0')/Decimal('1.609'),
        'km':         Decimal('1.0')/Decimal('1.609'),
        'k':          Decimal('1.0')/Decimal('1.609'),
    }
    for unit in units:
        Unit.objects.create(owner=None, name=unit, distance=units[unit]).save()

from datetime import date, timedelta
from workoutLogging.models import Workout

class WorkoutDay():
    def __init__(self, dateInstance, workouts):
        self.date = dateInstance
        self.workouts = workouts

    def dayOfWeekWorded(self):
        # The keys in this dictionary are based on what one would expect from
        # the output of date.isoweekday() [103, date Objects]
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

        return [(key, workoutTypes[key]) for key in workoutTypes]

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
        # Adding the name customized for PDF creation (see [102]) to the PDF
        # output
        flowables.append(Paragraph(self.user.userinfo.pdfName, dateStyle))
        flowables.append(Paragraph("", dateStyle))
        for day in self.days:
            flowables.append(Paragraph(str(day.date.strftime("%A, %B %d, %Y")), dateStyle))
            for workout in day.workouts:
                flowables.append(Paragraph("<strong>" + workout.title + " - " + prettydecimal(str(workout.distance)) + " miles" + (" - " + workout.wtype.name if workout.wtype != None else "") + (" - " + workout.shoe.name if workout.shoe != None else "") + "</strong>", workoutInfoStyle))
                # using <br/>'s from citation [24]
                flowables.append(Paragraph(workout.entry.replace("\r\n", "<br/>"), workoutEntryStyle))

        weekTotalStyle  = dateStyle
        statStyle       = workoutEntryStyle

        flowables.append(Paragraph("Week Totals", weekTotalStyle))
        for stat in self.getStats():
            flowables.append(Paragraph(stat[0] + ": " + prettydecimal(str(stat[1])), statStyle))

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

    # Accounting for days not in the month but will be displayed with the month
    # in the calendar; see [104]
    ####################################################################################
    #                                                                                  #

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

    #                                                                                  #
    ####################################################################################

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
        # These keys may be based on what the datetime [103] module uses for
        # numbers or each month
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

# This function gathers information to display on the calendar for a certain
# number of months before and after the current month. This helps in the
# scenario outlined in [69] where when the user scrolls far enough up or down in
# the calendar, we need to fetch more information to display on the calendar.
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





# CITATION [26]
from PIL import Image
def cropProfilePicture(pictureFile, format="full"):
    picture = Image.open(pictureFile)
    picture = picture.crop(
                            (
                                0 if picture.width < picture.height else (picture.width - picture.height) // 2,
                                0 if picture.height < picture.width else (picture.height - picture.width) // 2,
                                picture.width if picture.width < picture.height else (picture.width - (picture.width - picture.height) // 2),
                                picture.height if picture.height < picture.width else (picture.height - (picture.height - picture.width) // 2),
                            )
    )
    picture = picture.resize((400, 400) if format == "full" else (70, 70))
    return picture
# END CITATION

# NAME OF NEXT FUNCTION IS DERIVED FROM CITATION [44], CREATING FUNCTION FOR BLAST EMAIL IS FROM CITATION [46]
def blastEmail(sender, text, title, recipients=None):
    users = User.objects.all() if recipients == None else recipients
    for user in users:
        # NEXT time.sleep() CALL FROM CITATION [45]
        time.sleep(.3)
        try:
            if not user.userinfo.invalidEmailAddress:
                result = send_mail(title, text, sender, [user.email])
                if result == 0:
                    print("send failed for " + user.username)
        except:
            print("send failed for " + user.username)
