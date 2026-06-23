"""JWT authentication utilities."""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from smart_port_common.config import get_settings

security = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    sub: str
    email: str | None = None
    roles: list[str] = []
    exp: datetime | None = None


def create_token(
    subject: str,
    email: str | None = None,
    roles: list[str] | None = None,
    expires_hours: int = 24,
) -> str:
    settings = get_settings()
    payload: dict[str, Any] = {
        "sub": subject,
        "email": email,
        "roles": roles or [],
        "iss": settings.jwt_issuer,
        "exp": datetime.now(UTC) + timedelta(hours=expires_hours),
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_token(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
) -> TokenPayload:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
        )
        return TokenPayload(**payload)
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def require_roles(*required_roles: str):
    def checker(token: TokenPayload = Security(verify_token)) -> TokenPayload:
        if not any(role in token.roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return token

    return checker
