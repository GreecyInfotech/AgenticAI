from __future__ import annotations

from typing import Protocol

from ai_platform.domain.pricing.entities import PricingEntity


class PricingRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> PricingEntity | None: ...
    async def save(self, entity: PricingEntity) -> None: ...
