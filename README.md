# Lambda Service
This is a prototype app that utilizes Langchain and OpenAPI Assistants API to generate instagram post texts related to incoming  
internationally recognized days related to mental health and all things around psychology or internal development.
Generated Instagram post text can be adjusted (via like a regular char UI) to meet user needs.

## Code organization
### app.py
Contains the infrastructure code written in CDK that will be deployed to AWS

### config.py
Contains the configuration used by the infrastructure and the application code. The current setup expects the API keys to be stored in Secrets Manager under the name `api-keys`. For example, the secrets in the AWS console will look like this:
```json
{
    "openai-api-key": "<api-key-value>"
}
```

### getDaysLambda.py and generatePostLambda.py
Lambda handler that processes the incoming request and calls the LLM chain to generate a reply. 
These handlers use some helping function which were extracted to avoid much duplication.


### findRelevantDaysFromCalendar.py and generateInstagramPost.py
core logic of app

## Deploying to AWS

Clone the repository
```bash
git clone https://github.com/jmilkiewicz/LangChainOnAWSLambda.git
```


Install the dependencies; this creates a Conda env named `langchain-aws-service` and activates it.
```bash
conda deactivate
conda env create -f environment.yml # only needed once
conda activate langchain-aws-service
```

Bundle the code for Lambda deployment.
```bash
./bundle.sh
```

Deploy to your AWS account. These steps require that you must have configured the AWS credentials on your machine using the AWS CLI and using an account that has permissions to deploy and create infrastructure. See the [AWS CLI setup page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) and the [CDK guide](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) to learn more.
```bash
cdk bootstrap # Only needed once, if you have not used CDK before in your account
cdk deploy
```
After you run the above commands, you will see a list of assets that this code will generate and you will be asked whether you want to proceed. Enter `y` to go ahead with the deployment. Copy and save the API URL generated from the deployment; this will be used when you create the Slack app.

## Executing the API
Note the api-id from the deployment step. This is the first part in the endpoint URL generated from the deployment. For example, api-id is `xxxxxxx` in the endpoint URL `https://xxxxxxx.execute-api.eu-west-1.amazonaws.com/prod/`.

Get the resource id.
```bash
aws apigateway get-resources --rest-api-id <api-id> --output=text
# you will see an output like this, copy the resource id value, which is 789ai1gbjn in this sample
#ITEMS   imt3qkw2de              /
#ITEMS   njm8xp  imt3qkw2de      /generatePost   generatePost
```

Invoke the  api (easier with GET ,so with resource-id being _imt3qkw2de_ but it returns HTML here) 
```bash
aws apigateway test-invoke-method --rest-api-id <api-id> \
    --http-method GET \
    --path-with-query-string "?month=3" \
    --resource-id <resource-id> \
    --output json
```


