from __future__ import annotations

from ai_platform.application.commands.reserve_inventory import ReserveInventoryCommand
from ai_platform.application.dto.inventory_dto import ReserveInventoryResponseDTO
from ai_platform.config.dependencies import get_inventory_repository
from shared.logging import get_logger

logger = get_logger(__name__)


class ReserveInventoryHandler:
    def __init__(self) -> None:
        self._inventory = get_inventory_repository()

    async def handle(self, command: ReserveInventoryCommand) -> ReserveInventoryResponseDTO:
        result = await self._inventory.reserve(command.sku, command.quantity, command.order_id)
        logger.info("inventory_reserved_via_handler", sku=command.sku, order_id=command.order_id)
        return ReserveInventoryResponseDTO(**result)
