from __future__ import annotations

from typing import Protocol

from ai_platform.domain.shipment.entities import ShipmentEntity


class ShipmentRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> ShipmentEntity | None: ...
    async def save(self, entity: ShipmentEntity) -> None: ...
