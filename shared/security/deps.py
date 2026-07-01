from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.exceptions import ForbiddenError, UnauthorizedError
from shared.security.jwt import decode_token, has_permission

_bearer = HTTPBearer(auto_error=False)


class CurrentUser:
    def __init__(self, subject: str, role: str, claims: dict) -> None:
        self.subject = subject
        self.role = role
        self.claims = claims


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser:
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError()
    claims = decode_token(credentials.credentials)
    subject = claims.get("sub")
    if not subject:
        raise UnauthorizedError("Token missing subject")
    return CurrentUser(subject=str(subject), role=str(claims.get("role", "viewer")), claims=claims)


def require_permission(permission: str):
    async def _checker(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if not has_permission(user.role, permission):
            raise ForbiddenError(f"Permission '{permission}' required")
        return user

    return _checker


async def optional_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser | None:
    if credentials is None or not credentials.credentials:
        return None
    try:
        return await get_current_user(credentials)
    except (UnauthorizedError, HTTPException):
        return None
