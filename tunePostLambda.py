import json
from openai import OpenAI
from getApiKey import getApiKey
from tunePost import tunePost


def handler(event, context):
    print(f"event is {event}")
    body = json.loads(event["body"])

    client = OpenAI(api_key=getApiKey())

    response = tunePost(client, body)

    return build_response(response)


def build_response(response):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }
