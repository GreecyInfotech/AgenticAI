from __future__ import annotations

from typing import Any

from ai_platform.infrastructure.crm.base import CrmAccount
from ai_platform.infrastructure.repositories import CustomerRepository
from shared.exceptions import NotFoundError
from shared.logging import get_logger

logger = get_logger(__name__)

_memory_accounts: dict[str, CrmAccount] = {
    "CUST-001": CrmAccount(
        customer_id="CUST-001",
        name="Demo Distributor",
        tier="gold",
        account_manager="Jane Doe",
        email="demo@distributor.local",
        credit_limit=50000.0,
    )
}


class MockCrmClient:
    provider_name = "mock"

    def __init__(self) -> None:
        self._customers = CustomerRepository()

    async def get_account(self, customer_id: str) -> CrmAccount:
        if customer_id in _memory_accounts:
            return _memory_accounts[customer_id]
        try:
            row = await self._customers.get_by_id(customer_id)
            return CrmAccount(
                customer_id=row["customer_id"],
                name=row["name"],
                tier=row.get("tier", "standard"),
                credit_limit=float(row.get("credit_limit", 0.0)),
                account_manager="Unassigned",
            )
        except NotFoundError:
            raise

    async def update_account(self, customer_id: str, data: dict[str, Any]) -> CrmAccount:
        account = await self.get_account(customer_id)
        updated = account.model_copy(update={k: v for k, v in data.items() if k in CrmAccount.model_fields})
        _memory_accounts[customer_id] = updated
        logger.info("crm_account_updated", customer_id=customer_id, provider=self.provider_name)
        return updated

    async def search_accounts(self, query: str, *, limit: int = 10) -> list[CrmAccount]:
        query_lower = query.lower()
        results = [
            account
            for account in _memory_accounts.values()
            if query_lower in account.name.lower() or query_lower in account.customer_id.lower()
        ]
        if results:
            return results[:limit]
        customers = await self._customers.list_customers(limit=limit, offset=0)
        return [
            CrmAccount(
                customer_id=row["customer_id"],
                name=row["name"],
                tier=row.get("tier", "standard"),
                credit_limit=float(row.get("credit_limit", 0.0)),
            )
            for row in customers
            if query_lower in row["name"].lower()
        ][:limit]
