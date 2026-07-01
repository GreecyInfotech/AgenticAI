from __future__ import annotations

from typing import Any

from ai_platform.application.dto.customer_dto import CustomerResponseDTO
from ai_platform.application.dto.inventory_dto import InventoryResponseDTO
from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.application.dto.product_dto import ProductResponseDTO


def to_order_dto(order: dict[str, Any]) -> OrderResponseDTO:
    return OrderResponseDTO(
        order_id=order["order_id"],
        customer_id=order["customer_id"],
        status=order["status"],
        total=float(order["total"]),
        items=order["items"],
    )


def to_customer_dto(customer: dict[str, Any]) -> CustomerResponseDTO:
    return CustomerResponseDTO(
        customer_id=customer["customer_id"],
        name=customer["name"],
        tier=customer.get("tier", "standard"),
        credit_limit=float(customer.get("credit_limit", 0.0)),
    )


def to_product_dto(product: dict[str, Any]) -> ProductResponseDTO:
    return ProductResponseDTO(
        sku=product["sku"],
        name=product["name"],
        price=float(product["price"]),
        category=product.get("category", "general"),
    )


def to_inventory_dto(item: dict[str, Any]) -> InventoryResponseDTO:
    return InventoryResponseDTO(
        sku=item["sku"],
        available=int(item["available"]),
        warehouse=item.get("warehouse", "WH-01"),
    )
