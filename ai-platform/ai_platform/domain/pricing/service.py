from __future__ import annotations

from ai_platform.domain.pricing.entities import PricingEntity
from ai_platform.domain.pricing.repository import PricingRepository


class PricingService:
    def __init__(self, repository: PricingRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> PricingEntity | None:
        return await self._repository.get_by_id(entity_id)
