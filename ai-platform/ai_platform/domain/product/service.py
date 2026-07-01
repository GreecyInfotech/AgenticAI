from __future__ import annotations

from ai_platform.domain.product.entities import ProductEntity
from ai_platform.domain.product.repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> ProductEntity | None:
        return await self._repository.get_by_id(entity_id)
