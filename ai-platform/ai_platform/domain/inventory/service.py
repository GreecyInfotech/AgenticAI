from __future__ import annotations

from ai_platform.domain.inventory.entities import InventoryEntity
from ai_platform.domain.inventory.repository import InventoryRepository


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> InventoryEntity | None:
        return await self._repository.get_by_id(entity_id)
