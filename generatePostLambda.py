import json
import os

import requests

import config

from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from generateInstagramPost import generateInstagramPost


def handler(event, context):
    print(f"event is {event}")

    print(f"event is {event}")
    body = json.loads(event["body"])

    # validate_response = validate_inputs(body)
    # if validate_response:
    #     return validate_response

    date = body['date']
    name = body["name"]

    print(f"date is {date}")
    print(f"name is {name}")

    model = ChatOpenAI(temperature=0.0, model="gpt-4o", openai_api_key=get_api_key()).configurable_fields(
        temperature=ConfigurableField(
            id="llm_temperature",
            name="LLM Temperature",
            description="The temperature of the LLM",
        )
    )

    content = generateInstagramPost(model, body)
    return build_response(content)


def build_response(content):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"post": content})
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
