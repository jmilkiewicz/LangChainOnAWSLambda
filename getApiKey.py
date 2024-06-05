import config
import requests
import json
import os

def getApiKey():
    """Fetches the api keys saved in Secrets Manager"""

    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_extension_endpoint = "http://localhost:2773" + \
                                 "/secretsmanager/get?secretId=" + \
                                 config.config.API_KEYS_SECRET_NAME

    r = requests.get(secrets_extension_endpoint, headers=headers)
    secret = json.loads(json.loads(r.text)["SecretString"])

    return secret["openai-api-key"]

