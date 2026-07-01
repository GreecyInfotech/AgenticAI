from __future__ import annotations

"""AI platform security extensions — delegates core auth to shared.security."""

from shared.security.deps import CurrentUser, get_current_user, require_permission
from shared.security.jwt import ROLE_PERMISSIONS, create_access_token, decode_token, has_permission
from shared.security.pii import mask_pii, mask_pii_in_dict
from shared.security.prompt_injection import is_prompt_injection

from ai_platform.security.oauth import OAuthClient
from ai_platform.security.okta import OktaValidator

PERMISSIONS = ROLE_PERMISSIONS

__all__ = [
    "CurrentUser",
    "OAuthClient",
    "OktaValidator",
    "PERMISSIONS",
    "create_access_token",
    "decode_token",
    "get_current_user",
    "has_permission",
    "is_prompt_injection",
    "mask_pii",
    "mask_pii_in_dict",
    "require_permission",
]
