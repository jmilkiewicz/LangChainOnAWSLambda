import chevron

from findRelevantDaysFromCalendar import findRelevantDays
from sendEmail import send_email


def buildHtmlEmailBody(days):
    return fromTemplate(days, "email-html.mustache")


def buildTxtEmailBody(days):
    return fromTemplate(days, "email-txt.mustache")


def fromTemplate(model, tmplFile='email.mustache'):
    with open('templates/%s' % tmplFile, 'r') as f:
        return chevron.render(f, model)


def buildTxtNoEventsEmailBody(fromD, toDateD):
    return fromTemplate({'from': fromD, 'to': toDateD}, "email-no-events-txt.mustache")


def buildHtmlNoEventsEmailBody(fromD, toDateD):
    return fromTemplate({'from': fromD, 'to': toDateD}, "email-no-events-html.mustache")


def doNotify(model, fromDate, toDate):
    fromD = fromDate.strftime("%d, %b %Y")
    toDateD = toDate.strftime("%d, %b %Y")
    days = findRelevantDays(model, fromDate, toDate)

    subject = f'Nadchodzące ({fromD} - {toDateD}) eventy do ogłoszenia na instagram'
    if days:
        daysDict = [relevantDay.dict() for relevantDay in days]
        send_email(subject=subject, body_html=buildHtmlEmailBody(daysDict),
                   body_txt=buildTxtEmailBody(daysDict),
                   to="jmilkiewicz@gmail.com")
    else:

        print(f'nie ma eventów {fromD} - {toDateD}')
        send_email(subject=subject, body_html=buildHtmlNoEventsEmailBody(fromD, toDateD),
                   body_txt=buildTxtNoEventsEmailBody(fromD, toDateD),
                   to="jmilkiewicz@gmail.com")
