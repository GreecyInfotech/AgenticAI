from __future__ import annotations

from pydantic import BaseModel, Field

from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.config.dependencies import get_inventory_repository, get_order_repository, get_product_repository
from shared.constants.status import ORDER_STATUS_CREATED
from shared.exceptions import ValidationError
from shared.logging import get_logger
from shared.messaging import OrderCreatedEvent, publish

logger = get_logger(__name__)


class OrderItemInput(BaseModel):
    sku: str
    quantity: int = Field(ge=1)


class PlaceOrderCommand(BaseModel):
    customer_id: str
    items: list[OrderItemInput]


class PlaceOrderHandler:
    def __init__(self) -> None:
        self._orders = get_order_repository()
        self._products = get_product_repository()
        self._inventory = get_inventory_repository()

    async def handle(self, command: PlaceOrderCommand) -> OrderResponseDTO:
        if not command.items:
            raise ValidationError("Order must contain at least one item")

        total = 0.0
        resolved_items: list[dict] = []
        for item in command.items:
            product = await self._products.get_by_sku(item.sku)
            if product is None:
                raise ValidationError(f"Unknown product SKU: {item.sku}")
            line_total = product["price"] * item.quantity
            total += line_total
            resolved_items.append(
                {"sku": item.sku, "quantity": item.quantity, "unit_price": product["price"], "line_total": line_total}
            )

        order = await self._orders.create(command.customer_id, resolved_items, total)
        for item in command.items:
            await self._inventory.reserve(item.sku, item.quantity, order_id=order["order_id"])
        event = OrderCreatedEvent.create(
            order_id=order["order_id"],
            customer_id=command.customer_id,
            total=total,
            items=resolved_items,
        )
        await publish(event.event_type, event)
        logger.info("place_order_completed", order_id=order["order_id"], total=total)
        return OrderResponseDTO(
            order_id=order["order_id"],
            customer_id=command.customer_id,
            status=ORDER_STATUS_CREATED,
            total=total,
            items=resolved_items,
        )
