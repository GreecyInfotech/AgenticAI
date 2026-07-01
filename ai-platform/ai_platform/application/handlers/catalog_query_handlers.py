from __future__ import annotations

from ai_platform.application.dto.inventory_dto import InventoryResponseDTO
from ai_platform.application.dto.product_dto import ProductResponseDTO
from ai_platform.application.handlers.mappers import to_inventory_dto, to_product_dto
from ai_platform.application.queries.catalog_queries import GetInventoryQuery, ListProductsQuery
from ai_platform.config.dependencies import get_inventory_repository, get_product_repository
from shared.messaging import InventoryCheckedEvent, publish


class ListProductsHandler:
    def __init__(self) -> None:
        self._products = get_product_repository()

    async def handle(self, query: ListProductsQuery) -> list[ProductResponseDTO]:
        products = await self._products.list_products(limit=query.limit, offset=query.offset)
        return [to_product_dto(product) for product in products]


class GetInventoryHandler:
    def __init__(self) -> None:
        self._inventory = get_inventory_repository()

    async def handle(self, query: GetInventoryQuery) -> InventoryResponseDTO:
        item = await self._inventory.get_by_sku(query.sku)
        event = InventoryCheckedEvent.create(sku=query.sku, available=item["available"])
        await publish(event.event_type, event)
        return to_inventory_dto(item)
