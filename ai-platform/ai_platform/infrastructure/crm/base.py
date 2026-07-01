from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, Field


class CrmAccount(BaseModel):
    customer_id: str
    name: str
    tier: str = "standard"
    account_manager: str = ""
    email: str = ""
    phone: str = ""
    credit_limit: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class CrmClient(Protocol):
    async def get_account(self, customer_id: str) -> CrmAccount: ...

    async def update_account(self, customer_id: str, data: dict[str, Any]) -> CrmAccount: ...

    async def search_accounts(self, query: str, *, limit: int = 10) -> list[CrmAccount]: ...
