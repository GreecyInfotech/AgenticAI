from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from shared.config.settings import get_base_settings
from shared.exceptions import UnauthorizedError

ROLES = ("admin", "sales_rep", "distributor", "viewer")
ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "admin": frozenset(
        {
            "orders:read",
            "orders:write",
            "inventory:read",
            "customers:read",
            "customers:write",
            "conversation:write",
            "analytics:read",
        }
    ),
    "sales_rep": frozenset(
        {
            "orders:read",
            "orders:write",
            "inventory:read",
            "customers:read",
            "conversation:write",
        }
    ),
    "distributor": frozenset(
        {
            "orders:read",
            "orders:write",
            "inventory:read",
            "customers:read",
            "conversation:write",
        }
    ),
    "viewer": frozenset({"orders:read", "inventory:read", "customers:read"}),
}


def create_access_token(subject: str, *, role: str = "distributor", extra: dict[str, Any] | None = None) -> str:
    settings = get_base_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "role": role, "exp": expire}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    settings = get_base_settings()
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, frozenset())
