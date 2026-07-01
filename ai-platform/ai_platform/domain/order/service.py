from __future__ import annotations

from ai_platform.domain.order.entities import OrderEntity
from ai_platform.domain.order.repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> OrderEntity | None:
        return await self._repository.get_by_id(entity_id)
