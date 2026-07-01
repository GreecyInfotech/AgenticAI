from __future__ import annotations

from typing import Protocol

from ai_platform.domain.customer.entities import CustomerEntity


class CustomerRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> CustomerEntity | None: ...
    async def save(self, entity: CustomerEntity) -> None: ...
