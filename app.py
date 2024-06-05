from aws_cdk import (
    App, Duration, Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager
)
import config


class LangChainApp(Stack):
    def __init__(self, app: App, id: str) -> None:
        super().__init__(app, id)

        handler = lambda_.Function(self, "LlmInstagramDayPostProducer",
                                   runtime=lambda_.Runtime.PYTHON_3_12,
                                   code=lambda_.Code.from_asset("dist/lambda.zip"),
                                   handler="main.handler",
                                   layers=[
                                       lambda_.LayerVersion.from_layer_version_arn(
                                           self,
                                           "SecretsExtensionLayer",
                                           layer_version_arn=config.config.SECRETS_EXTENSION_ARN
                                       )
                                   ],
                                   timeout=Duration.minutes(5)
                                   )

        secret = secretsmanager.Secret.from_secret_name_v2(self, 'secret', config.config.API_KEYS_SECRET_NAME)
        secret.grant_read(handler)
        secret.grant_write(handler)

        api = apigateway.RestApi(self, "insta-day-posts-api",
                                 rest_api_name="Api for generating Insta posts ",
                                 description="Showcases langchain use of llm models"
                                 )

        # request_model = api.add_model("RequestModel", content_type="application/json",
        #                               model_name="RequestModel",
        #                               description="Schema for request payload",
        #                               schema={
        #                                   "title": "requestParameters",
        #                                   "type": apigateway.JsonSchemaType.OBJECT,
        #                                   "properties": {
        #                                       "prompt": {
        #                                           "type": apigateway.JsonSchemaType.STRING
        #                                       },
        #                                       "postContent": {
        #                                           "type": apigateway.JsonSchemaType.STRING
        #                                       }
        #                                   }
        #                               }
        #                               )

        get_days = apigateway.LambdaIntegration(handler)

        # api.root.add_method(
        #     "POST",
        #     post_integration,
        #     authorization_type=apigateway.AuthorizationType.IAM,
        #     request_models={
        #         "application/json": request_model
        #     },
        #     request_validator_options={
        #         "request_validator_name": 'request-validator',
        #         "validate_request_body": True,
        #         "validate_request_parameters": False
        #     }
        # )

        api.root.add_method(
            "GET",
            get_days
        )

        # api.root.add_method(
        #     "GET",
        #     get_days,
        #     authorization_type=apigateway.AuthorizationType.IAM,
        #     request_models={
        #         "application/json": request_model
        #     },
        #     request_validator_options={
        #         "request_validator_name": 'request-validator',
        #         "validate_request_body": True,
        #         "validate_request_parameters": False
        #     }
        # )


app = App()
LangChainApp(app, "InstagramDayPostApp")
app.synth()
