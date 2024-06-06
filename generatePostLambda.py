import json
from openai import OpenAI
from getApiKey import getApiKey
from generateInstagramPost import generateInstagramPost


def handler(event, context):
    print(f"event is {event}")

    print(f"event is {event}")
    body = json.loads(event["body"])

    # TODO add/check validation
    # validate_response = validate_inputs(body)
    # if validate_response:
    #     return validate_response

    date = body['date']
    name = body["name"]

    print(f"date is {date}")
    print(f"name is {name}")

    client = OpenAI(api_key=getApiKey())

    content = generateInstagramPost(client, body)

    return build_response(content)


def build_response(content):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"post": content})
    }
