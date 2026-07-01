from __future__ import annotations

from typing import Protocol

from ai_platform.domain.inventory.entities import InventoryEntity


class InventoryRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> InventoryEntity | None: ...
    async def save(self, entity: InventoryEntity) -> None: ...
