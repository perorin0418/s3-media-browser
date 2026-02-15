from aws_cdk import App
from aws_cdk.assertions import Template

from cdk_config.auth_settings import (
    DEFAULT_CALLBACK_URLS,
    DEFAULT_HOSTED_UI_DOMAIN_PREFIX,
    DEFAULT_LOGOUT_URLS,
    SSM_CLIENT_ID_PARAM,
    SSM_HOSTED_UI_DOMAIN_PARAM,
    resolve_auth_settings,
)
from cdk_stacks.auth_stack import AuthStack


def test_auth_stack_resources() -> None:
    app = App()
    settings = resolve_auth_settings(None)
    stack = AuthStack(app, "AuthStack", settings=settings)
    template = Template.from_stack(stack)

    template.resource_count_is("AWS::Cognito::UserPool", 1)
    template.resource_count_is("AWS::Cognito::UserPoolClient", 1)
    template.resource_count_is("AWS::Cognito::UserPoolDomain", 1)

    template.has_resource_properties(
        "AWS::Cognito::UserPoolClient",
        {
            "CallbackURLs": DEFAULT_CALLBACK_URLS,
            "LogoutURLs": DEFAULT_LOGOUT_URLS,
            "SupportedIdentityProviders": ["COGNITO"],
        },
    )

    template.has_resource_properties(
        "AWS::Cognito::UserPoolDomain",
        {
            "Domain": DEFAULT_HOSTED_UI_DOMAIN_PREFIX,
        },
    )

    template.has_resource_properties(
        "AWS::SSM::Parameter",
        {
            "Name": SSM_HOSTED_UI_DOMAIN_PARAM,
            "Type": "String",
        },
    )

    template.has_resource_properties(
        "AWS::SSM::Parameter",
        {
            "Name": SSM_CLIENT_ID_PARAM,
            "Type": "String",
        },
    )
