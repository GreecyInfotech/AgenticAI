from __future__ import annotations

from ai_platform.domain.promotion.entities import PromotionEntity
from ai_platform.domain.promotion.repository import PromotionRepository


class PromotionService:
    def __init__(self, repository: PromotionRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> PromotionEntity | None:
        return await self._repository.get_by_id(entity_id)
