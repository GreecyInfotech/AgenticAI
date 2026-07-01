from __future__ import annotations

from ai_platform.application.commands.cancel_order import CancelOrderCommand
from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.application.handlers.mappers import to_order_dto
from ai_platform.config.dependencies import get_inventory_repository, get_order_repository
from shared.constants.status import ORDER_STATUS_CREATED
from shared.exceptions import ConflictError, ForbiddenError
from shared.logging import get_logger
from shared.messaging import OrderCancelledEvent, publish

logger = get_logger(__name__)

_CANCELLABLE_STATUSES = {ORDER_STATUS_CREATED}


class CancelOrderHandler:
    def __init__(self) -> None:
        self._orders = get_order_repository()
        self._inventory = get_inventory_repository()

    async def handle(self, command: CancelOrderCommand) -> OrderResponseDTO:
        order = await self._orders.get_by_id(command.order_id)
        if order["customer_id"] != command.customer_id:
            raise ForbiddenError("Cannot cancel another customer's order")
        if order["status"] not in _CANCELLABLE_STATUSES:
            raise ConflictError(
                f"Order {command.order_id} cannot be cancelled in status '{order['status']}'"
            )

        for item in order["items"]:
            sku = item["sku"] if isinstance(item, dict) else item.sku
            quantity = item["quantity"] if isinstance(item, dict) else item.quantity
            await self._inventory.release(sku, int(quantity), order_id=command.order_id)

        updated = await self._orders.cancel(command.order_id, command.reason)
        event = OrderCancelledEvent.create(order_id=command.order_id, reason=command.reason)
        await publish(event.event_type, event)
        logger.info("order_cancelled", order_id=command.order_id, reason=command.reason)
        return to_order_dto(updated)
