from __future__ import annotations

from ai_platform.domain.shipment.entities import ShipmentEntity
from ai_platform.domain.shipment.repository import ShipmentRepository


class ShipmentService:
    def __init__(self, repository: ShipmentRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> ShipmentEntity | None:
        return await self._repository.get_by_id(entity_id)
