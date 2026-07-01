from __future__ import annotations

from typing import Protocol

from ai_platform.domain.promotion.entities import PromotionEntity


class PromotionRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> PromotionEntity | None: ...
    async def save(self, entity: PromotionEntity) -> None: ...
