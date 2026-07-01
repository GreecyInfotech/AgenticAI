from __future__ import annotations

from typing import Protocol

from ai_platform.domain.order.entities import OrderEntity


class OrderRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> OrderEntity | None: ...
    async def save(self, entity: OrderEntity) -> None: ...
