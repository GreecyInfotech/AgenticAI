from __future__ import annotations

from ai_platform.application.dto.conversation_dto import ConversationRequestDTO, ConversationResponseDTO
from ai_platform.application.dto.customer_dto import CustomerResponseDTO
from ai_platform.application.dto.inventory_dto import (
    InventoryResponseDTO,
    ReserveInventoryRequestDTO,
    ReserveInventoryResponseDTO,
)
from ai_platform.application.dto.order_dto import CreateOrderRequestDTO, OrderItemDTO, OrderResponseDTO
from ai_platform.application.dto.product_dto import ProductResponseDTO

__all__ = [
    "ConversationRequestDTO",
    "ConversationResponseDTO",
    "CreateOrderRequestDTO",
    "CustomerResponseDTO",
    "InventoryResponseDTO",
    "OrderItemDTO",
    "OrderResponseDTO",
    "ProductResponseDTO",
    "ReserveInventoryRequestDTO",
    "ReserveInventoryResponseDTO",
]
