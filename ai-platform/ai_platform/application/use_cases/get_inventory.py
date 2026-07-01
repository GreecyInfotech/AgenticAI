from __future__ import annotations

from ai_platform.application.commands.reserve_inventory import ReserveInventoryCommand
from ai_platform.application.dto.inventory_dto import InventoryResponseDTO, ReserveInventoryResponseDTO
from ai_platform.application.handlers.catalog_query_handlers import GetInventoryHandler
from ai_platform.application.handlers.reserve_inventory_handler import ReserveInventoryHandler
from ai_platform.application.queries.catalog_queries import GetInventoryQuery


class GetInventoryUseCase:
    def __init__(self) -> None:
        self._handler = GetInventoryHandler()

    async def execute(self, sku: str) -> InventoryResponseDTO:
        return await self._handler.handle(GetInventoryQuery(sku=sku))


class ReserveInventoryUseCase:
    def __init__(self) -> None:
        self._handler = ReserveInventoryHandler()

    async def execute(self, sku: str, quantity: int, order_id: str) -> ReserveInventoryResponseDTO:
        command = ReserveInventoryCommand(sku=sku, quantity=quantity, order_id=order_id)
        return await self._handler.handle(command)
