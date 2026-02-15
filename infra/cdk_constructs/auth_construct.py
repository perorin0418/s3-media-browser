from aws_cdk import Stack, aws_cognito as cognito, aws_ssm as ssm
from constructs import Construct

from cdk_config.auth_settings import AuthSettings


class AuthConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, settings: AuthSettings) -> None:
        super().__init__(scope, construct_id)

        user_pool = cognito.UserPool(
            self,
            "UserPool",
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
        )

        user_pool_client = cognito.UserPoolClient(
            self,
            "UserPoolClient",
            user_pool=user_pool,
            generate_secret=False,
            auth_flows=cognito.AuthFlow(user_srp=True),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.PROFILE,
                ],
                callback_urls=settings.callback_urls,
                logout_urls=settings.logout_urls,
            ),
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO,
            ],
        )

        user_pool.add_domain(
            "HostedUiDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=settings.domain_prefix,
            ),
        )

        stack_region = Stack.of(self).region
        hosted_ui_domain = (
            f"https://{settings.domain_prefix}.auth.{stack_region}.amazoncognito.com"
        )

        ssm.StringParameter(
            self,
            "HostedUiDomainParameter",
            parameter_name=settings.hosted_ui_domain_param,
            string_value=hosted_ui_domain,
        )

        ssm.StringParameter(
            self,
            "HostedUiClientIdParameter",
            parameter_name=settings.client_id_param,
            string_value=user_pool_client.user_pool_client_id,
        )
