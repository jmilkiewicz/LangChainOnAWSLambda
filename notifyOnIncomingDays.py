from sendEmail import send_email
import chevron
from findRelevantDaysFromCalendar import findRelevantDays


def buildEmailBody(days):
    with open('templates/email.mustache', 'r') as f:
        return chevron.render(f, days)


def doNotify(model, fromDate, toDate):
    days = findRelevantDays(model, fromDate, toDate)
    if days:
        daysDict = [ relevantDay.dict() for relevantDay in days]
        send_email(subject="Nadchodzące eventy do ogłoszenia na instagram", body=buildEmailBody(daysDict),
                   to="jmilkiewicz@gmail.com")
    else:
        print(f'nie ma eventów {fromDate.strftime("%d, %b %Y")} - {fromDate.strftime("%d, %b %Y")}')
