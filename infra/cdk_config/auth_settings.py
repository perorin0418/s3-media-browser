from dataclasses import dataclass
from typing import Dict, List, Optional

DEFAULT_CALLBACK_URLS: List[str] = [
    "http://localhost:3000/auth/callback",
]
DEFAULT_LOGOUT_URLS: List[str] = [
    "http://localhost:3000/",
]

DEFAULT_HOSTED_UI_DOMAIN_PREFIX = "s3-media-browser-auth"

AUTH_CALLBACK_URLS_BY_STAGE: Dict[str, List[str]] = {
    "dev": DEFAULT_CALLBACK_URLS,
}
AUTH_LOGOUT_URLS_BY_STAGE: Dict[str, List[str]] = {
    "dev": DEFAULT_LOGOUT_URLS,
}

SSM_HOSTED_UI_DOMAIN_PARAM = "/s3-media-browser/auth/hosted-ui-domain"
SSM_CLIENT_ID_PARAM = "/s3-media-browser/auth/client-id"


@dataclass(frozen=True)
class AuthSettings:
    callback_urls: List[str]
    logout_urls: List[str]
    domain_prefix: str
    hosted_ui_domain_param: str
    client_id_param: str


def resolve_auth_settings(stage: Optional[str]) -> AuthSettings:
    callback_urls = AUTH_CALLBACK_URLS_BY_STAGE.get(stage, DEFAULT_CALLBACK_URLS)
    logout_urls = AUTH_LOGOUT_URLS_BY_STAGE.get(stage, DEFAULT_LOGOUT_URLS)

    if stage:
        domain_prefix = f"{DEFAULT_HOSTED_UI_DOMAIN_PREFIX}-{stage}"
    else:
        domain_prefix = DEFAULT_HOSTED_UI_DOMAIN_PREFIX

    return AuthSettings(
        callback_urls=callback_urls,
        logout_urls=logout_urls,
        domain_prefix=domain_prefix,
        hosted_ui_domain_param=SSM_HOSTED_UI_DOMAIN_PARAM,
        client_id_param=SSM_CLIENT_ID_PARAM,
    )
