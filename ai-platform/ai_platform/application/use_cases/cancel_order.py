from __future__ import annotations

from ai_platform.application.commands.cancel_order import CancelOrderCommand
from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.application.handlers.cancel_order_handler import CancelOrderHandler


class CancelOrderUseCase:
    def __init__(self) -> None:
        self._handler = CancelOrderHandler()

    async def execute(self, order_id: str, customer_id: str, reason: str = "customer_requested") -> OrderResponseDTO:
        command = CancelOrderCommand(order_id=order_id, customer_id=customer_id, reason=reason)
        return await self._handler.handle(command)
