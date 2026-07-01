from __future__ import annotations

import httpx

from ai_platform.config.settings import get_settings
from shared.exceptions import UnauthorizedError
from shared.logging import get_logger

logger = get_logger(__name__)


class OAuthClient:
    """OAuth 2.0 token introspection client."""

    async def authenticate(self, token: str) -> dict | None:
        if not token:
            return None

        settings = get_settings()
        if not settings.oauth_issuer:
            return {"sub": "dev-user", "role": "distributor"}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{settings.oauth_issuer.rstrip('/')}/oauth/introspect",
                    data={"token": token},
                )
                response.raise_for_status()
                payload = response.json()
                if not payload.get("active"):
                    raise UnauthorizedError("Token is not active")
                return {"sub": payload.get("sub", ""), "role": payload.get("role", "distributor")}
        except UnauthorizedError:
            raise
        except Exception as exc:
            logger.warning("oauth_introspection_failed", error=str(exc))
            return None
