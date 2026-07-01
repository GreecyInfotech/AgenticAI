from __future__ import annotations

from typing import Any

import httpx

from ai_platform.config.settings import get_settings
from ai_platform.infrastructure.crm.base import CrmAccount
from shared.exceptions import NotFoundError, ServiceUnavailableError
from shared.logging import get_logger

logger = get_logger(__name__)


class RestCrmClient:
    """Generic REST CRM adapter (Salesforce/HubSpot/custom CRM via HTTP API)."""

    provider_name = "rest"

    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.crm_base_url.rstrip("/")
        self._api_key = settings.crm_api_key
        self._timeout = settings.crm_timeout_seconds

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    async def get_account(self, customer_id: str) -> CrmAccount:
        if not self._base_url:
            raise ServiceUnavailableError("CRM base URL is not configured")
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                f"{self._base_url}/accounts/{customer_id}",
                headers=self._headers(),
            )
            if response.status_code == 404:
                raise NotFoundError("crm_account", customer_id)
            response.raise_for_status()
            data = response.json()
            return CrmAccount(
                customer_id=data.get("customer_id", customer_id),
                name=data.get("name", ""),
                tier=data.get("tier", "standard"),
                account_manager=data.get("account_manager", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                credit_limit=float(data.get("credit_limit", 0.0)),
                metadata=data.get("metadata", {}),
            )

    async def update_account(self, customer_id: str, data: dict[str, Any]) -> CrmAccount:
        if not self._base_url:
            raise ServiceUnavailableError("CRM base URL is not configured")
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.patch(
                f"{self._base_url}/accounts/{customer_id}",
                headers=self._headers(),
                json=data,
            )
            response.raise_for_status()
            payload = response.json()
            return CrmAccount(**payload)

    async def search_accounts(self, query: str, *, limit: int = 10) -> list[CrmAccount]:
        if not self._base_url:
            raise ServiceUnavailableError("CRM base URL is not configured")
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                f"{self._base_url}/accounts/search",
                headers=self._headers(),
                params={"q": query, "limit": limit},
            )
            response.raise_for_status()
            items = response.json().get("items", [])
            return [CrmAccount(**item) for item in items]
