from __future__ import annotations

from typing import Any

from ai_platform.config.settings import get_settings
from ai_platform.infrastructure.crm.base import CrmAccount, CrmClient
from ai_platform.infrastructure.crm.mock_client import MockCrmClient
from ai_platform.infrastructure.crm.rest_client import RestCrmClient
from shared.logging import get_logger

logger = get_logger(__name__)

_client: CrmClient | None = None


def get_crm_client() -> CrmClient:
    global _client
    if _client is None:
        settings = get_settings()
        if settings.crm_provider == "rest" and settings.crm_base_url:
            _client = RestCrmClient()
        else:
            _client = MockCrmClient()
        logger.info("crm_client_initialized", provider=settings.crm_provider)
    return _client


async def lookup_crm_account(customer_id: str) -> CrmAccount:
    return await get_crm_client().get_account(customer_id)


async def search_crm_accounts(query: str, *, limit: int = 10) -> list[CrmAccount]:
    return await get_crm_client().search_accounts(query, limit=limit)


async def update_crm_account(customer_id: str, data: dict[str, Any]) -> CrmAccount:
    return await get_crm_client().update_account(customer_id, data)


async def check_crm_health() -> dict[str, str]:
    settings = get_settings()
    if settings.crm_provider == "rest" and settings.crm_base_url:
        try:
            import httpx

            async with httpx.AsyncClient(timeout=settings.crm_timeout_seconds) as client:
                response = await client.get(f"{settings.crm_base_url.rstrip('/')}/health")
                if response.status_code < 500:
                    return {"status": "UP", "provider": "rest"}
        except Exception as exc:
            return {"status": "DOWN", "provider": "rest", "detail": str(exc)}
    return {"status": "UP", "provider": settings.crm_provider, "mode": "mock"}
