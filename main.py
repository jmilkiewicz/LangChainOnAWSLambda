import json
import os
from typing import Dict

import requests

import chain
import config

from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

from findRelevantDaysFromCalendar import findRelevantDays


def handler(event, context):
    print(f"event is {event}")

    month = event.get("queryStringParameters",{}).get("months","")

    print(f"month is {month}")

    model = ChatOpenAI(temperature=0.0, model="gpt-4o", openai_api_key=get_api_key()).configurable_fields(
        temperature=ConfigurableField(
            id="llm_temperature",
            name="LLM Temperature",
            description="The temperature of the LLM",
        )
    )

    days = findRelevantDays(model, month)

    dicts = [relevantDay.dict()  for relevantDay in days]

    return build_response(dicts)


def build_response(body):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
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
