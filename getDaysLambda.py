import json
import os
from typing import Dict

import requests

import chain
import config

from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
import chevron

from findRelevantDaysFromCalendar import findRelevantDays


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

    model = ChatOpenAI(temperature=0.0, model="gpt-4o", openai_api_key=get_api_key()).configurable_fields(
        temperature=ConfigurableField(
            id="llm_temperature",
            name="LLM Temperature",
            description="The temperature of the LLM",
        )
    )

    days = findRelevantDays(model, month)

    dicts = [  {"event": relevantDay.dict()} | {"index":index} for index, relevantDay in enumerate(days)]

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


def get_api_key():
    """Fetches the api keys saved in Secrets Manager"""

    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_extension_endpoint = "http://localhost:2773" + \
                                 "/secretsmanager/get?secretId=" + \
                                 config.config.API_KEYS_SECRET_NAME

    r = requests.get(secrets_extension_endpoint, headers=headers)
    secret = json.loads(json.loads(r.text)["SecretString"])

    return secret["openai-api-key"]
