from __future__ import annotations

from typing import Protocol

from ai_platform.domain.product.entities import ProductEntity


class ProductRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> ProductEntity | None: ...
    async def save(self, entity: ProductEntity) -> None: ...
