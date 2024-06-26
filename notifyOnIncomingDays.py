from sendEmail import send_email
import chevron
from findRelevantDaysFromCalendar import findRelevantDays


def buildHtmlEmailBody(days):
    return fromTemplate(days, "email-html.mustache")


def buildTxtEmailBody(days):
    return fromTemplate(days, "email-txt.mustache")


def fromTemplate(days, tmplFile='email.mustache'):
    with open('templates/%s' % tmplFile, 'r') as f:
        return chevron.render(f, days)


def doNotify(model, fromDate, toDate):
    days = findRelevantDays(model, fromDate, toDate)
    if days:
        daysDict = [relevantDay.dict() for relevantDay in days]
        send_email(subject="Nadchodzące eventy do ogłoszenia na instagram", body_html=buildHtmlEmailBody(daysDict),
                   body_txt=buildTxtEmailBody(daysDict),
                   to="jmilkiewicz@gmail.com")
    else:
        print(f'nie ma eventów {fromDate.strftime("%d, %b %Y")} - {fromDate.strftime("%d, %b %Y")}')
