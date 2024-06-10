import chevron

from findRelevantDaysFromCalendar import findRelevantDays
from lllmModelBuilder import buildLLM
from getApiKey import getApiKey
from datetime import datetime, timedelta


def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


def handler(event, context):
    print(f"event is {event}")

    event = cleanNullTerms(event)

    month = event.get("queryStringParameters", {}).get("month", "")

    print(f"month is {month}")

    model = buildLLM(key=getApiKey(), temperature=0.0)

    days = findRelevantDays(model, datetime.now(), datetime.now() + timedelta(days=30))

    dicts = [{"event": relevantDay.dict()} | {"index": index} for index, relevantDay in enumerate(days)]

    return build_response(dicts)


def build_response(dicts):
    with open('templates/days.mustache', 'r') as f:
        body = chevron.render(f, dicts)
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": body
        }
