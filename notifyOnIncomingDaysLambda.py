from datetime import datetime, timedelta

from getApiKey import getApiKey
from lllmModelBuilder import buildLLM

from notifyOnIncomingDays import doNotify


def handler(event, context):
    model = buildLLM(key=getApiKey(), temperature=0.0)
    doNotify(model, datetime.now(), datetime.now() + timedelta(days=10))
    return build_response()


def build_response():
    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
    }
