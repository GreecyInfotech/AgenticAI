from __future__ import annotations

from ai_platform.application.dto.product_dto import ProductResponseDTO
from ai_platform.application.handlers.catalog_query_handlers import ListProductsHandler
from ai_platform.application.queries.catalog_queries import ListProductsQuery


class ListProductsUseCase:
    def __init__(self) -> None:
        self._handler = ListProductsHandler()

    async def execute(self, *, limit: int = 20, offset: int = 0) -> list[ProductResponseDTO]:
        return await self._handler.handle(ListProductsQuery(limit=limit, offset=offset))
