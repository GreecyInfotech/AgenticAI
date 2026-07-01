from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class OrderCreatedEvent(DomainEvent):
    event_type: str = "order.created"

    @classmethod
    def create(cls, order_id: str, customer_id: str, total: float, items: list[dict[str, Any]]) -> OrderCreatedEvent:
        return cls(payload={"order_id": order_id, "customer_id": customer_id, "total": total, "items": items})


class OrderUpdatedEvent(DomainEvent):
    event_type: str = "order.updated"

    @classmethod
    def create(cls, order_id: str, status: str) -> OrderUpdatedEvent:
        return cls(payload={"order_id": order_id, "status": status})


class OrderCancelledEvent(DomainEvent):
    event_type: str = "order.cancelled"

    @classmethod
    def create(cls, order_id: str, reason: str) -> OrderCancelledEvent:
        return cls(payload={"order_id": order_id, "reason": reason})


class InventoryCheckedEvent(DomainEvent):
    event_type: str = "inventory.checked"

    @classmethod
    def create(cls, sku: str, available: int) -> InventoryCheckedEvent:
        return cls(payload={"sku": sku, "available": available})


class InventoryReservedEvent(DomainEvent):
    event_type: str = "inventory.reserved"

    @classmethod
    def create(cls, sku: str, quantity: int, order_id: str) -> InventoryReservedEvent:
        return cls(payload={"sku": sku, "quantity": quantity, "order_id": order_id})


class PromotionAppliedEvent(DomainEvent):
    event_type: str = "promotion.applied"

    @classmethod
    def create(cls, order_id: str, promotion_code: str, discount: float) -> PromotionAppliedEvent:
        return cls(payload={"order_id": order_id, "promotion_code": promotion_code, "discount": discount})


class CreditCheckedEvent(DomainEvent):
    event_type: str = "credit.checked"

    @classmethod
    def create(cls, customer_id: str, approved: bool, limit: float) -> CreditCheckedEvent:
        return cls(payload={"customer_id": customer_id, "approved": approved, "credit_limit": limit})


class PaymentCompletedEvent(DomainEvent):
    event_type: str = "payment.completed"

    @classmethod
    def create(cls, order_id: str, amount: float, payment_id: str) -> PaymentCompletedEvent:
        return cls(payload={"order_id": order_id, "amount": amount, "payment_id": payment_id})


class ShipmentCreatedEvent(DomainEvent):
    event_type: str = "shipment.created"

    @classmethod
    def create(cls, order_id: str, shipment_id: str, carrier: str) -> ShipmentCreatedEvent:
        return cls(payload={"order_id": order_id, "shipment_id": shipment_id, "carrier": carrier})


class NotificationSentEvent(DomainEvent):
    event_type: str = "notification.sent"

    @classmethod
    def create(cls, channel: str, recipient: str, template: str) -> NotificationSentEvent:
        return cls(payload={"channel": channel, "recipient": recipient, "template": template})
