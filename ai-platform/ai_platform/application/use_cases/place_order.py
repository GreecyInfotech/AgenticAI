from __future__ import annotations

from ai_platform.application.commands.place_order import OrderItemInput, PlaceOrderCommand
from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.application.handlers.place_order_handler import PlaceOrderHandler


class PlaceOrderUseCase:
    def __init__(self) -> None:
        self._handler = PlaceOrderHandler()

    async def execute(self, customer_id: str, items: list[dict]) -> OrderResponseDTO:
        command = PlaceOrderCommand(
            customer_id=customer_id,
            items=[OrderItemInput(sku=i["sku"], quantity=int(i.get("quantity", 1))) for i in items],
        )
        return await self._handler.handle(command)
