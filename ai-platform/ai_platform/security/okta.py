from __future__ import annotations

import httpx

from ai_platform.config.settings import get_settings
from shared.exceptions import UnauthorizedError
from shared.logging import get_logger

logger = get_logger(__name__)


class OktaValidator:
    """Validates Okta JWT access tokens via OIDC userinfo."""

    async def validate(self, token: str) -> dict:
        settings = get_settings()
        if not settings.okta_domain:
            if not token:
                raise UnauthorizedError("Missing token")
            return {"sub": "dev-user", "role": "distributor"}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"https://{settings.okta_domain}/oauth2/v1/userinfo",
                    headers={"Authorization": f"Bearer {token}"},
                )
                response.raise_for_status()
                data = response.json()
                return {"sub": data.get("sub", ""), "role": data.get("role", "distributor")}
        except Exception as exc:
            logger.warning("okta_validation_failed", error=str(exc))
            raise UnauthorizedError("Invalid Okta token") from exc
