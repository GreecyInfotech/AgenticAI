from __future__ import annotations

from ai_platform.domain.customer.entities import CustomerEntity
from ai_platform.domain.customer.repository import CustomerRepository


class CustomerService:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> CustomerEntity | None:
        return await self._repository.get_by_id(entity_id)
