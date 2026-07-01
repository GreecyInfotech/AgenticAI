from __future__ import annotations

from shared.security.deps import CurrentUser, get_current_user, optional_user, require_permission
from shared.security.jwt import ROLE_PERMISSIONS, ROLES, create_access_token, decode_token, has_permission
from shared.security.pii import mask_pii, mask_pii_in_dict
from shared.security.prompt_injection import is_prompt_injection

__all__ = [
    "ROLE_PERMISSIONS",
    "ROLES",
    "CurrentUser",
    "create_access_token",
    "decode_token",
    "get_current_user",
    "has_permission",
    "is_prompt_injection",
    "mask_pii",
    "mask_pii_in_dict",
    "optional_user",
    "require_permission",
]
