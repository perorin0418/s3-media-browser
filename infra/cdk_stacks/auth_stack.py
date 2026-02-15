from aws_cdk import Stack
from constructs import Construct

from cdk_config.auth_settings import AuthSettings
from cdk_constructs.auth_construct import AuthConstruct


class AuthStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, *, settings: AuthSettings, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        AuthConstruct(self, "Auth", settings=settings)
