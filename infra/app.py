import os

from aws_cdk import App, Environment

from cdk_config.auth_settings import resolve_auth_settings
from cdk_stacks.auth_stack import AuthStack

app = App()

env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION"),
)

stage = app.node.try_get_context("stage")
settings = resolve_auth_settings(stage)

AuthStack(app, "AuthStack", settings=settings, env=env)

app.synth()
