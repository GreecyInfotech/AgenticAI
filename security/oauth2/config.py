"""OAuth2 / OIDC authentication configuration."""

from dataclasses import dataclass
from enum import Enum


class AuthProvider(str, Enum):
    LOCAL = "local"
    OKTA = "okta"
    AZURE_AD = "azure_ad"


@dataclass
class OAuth2Config:
    provider: AuthProvider
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: list[str]
    authorization_url: str
    token_url: str
    userinfo_url: str


PROVIDERS: dict[AuthProvider, dict] = {
    AuthProvider.OKTA: {
        "authorization_url": "https://{domain}/oauth2/v1/authorize",
        "token_url": "https://{domain}/oauth2/v1/token",
        "userinfo_url": "https://{domain}/oauth2/v1/userinfo",
        "scopes": ["openid", "profile", "email", "groups"],
    },
    AuthProvider.AZURE_AD: {
        "authorization_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/v1.0/me",
        "scopes": ["openid", "profile", "email", "User.Read"],
    },
}


def get_oauth2_config(provider: AuthProvider, **kwargs: str) -> OAuth2Config:
    template = PROVIDERS[provider]
    return OAuth2Config(
        provider=provider,
        client_id=kwargs.get("client_id", ""),
        client_secret=kwargs.get("client_secret", ""),
        redirect_uri=kwargs.get("redirect_uri", "http://localhost:8080/api/v1/auth/callback"),
        scopes=template["scopes"],
        authorization_url=template["authorization_url"].format(**kwargs),
        token_url=template["token_url"].format(**kwargs),
        userinfo_url=template["userinfo_url"].format(**kwargs),
    )
