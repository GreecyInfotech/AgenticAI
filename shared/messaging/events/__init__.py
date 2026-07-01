"""Kafka domain event schemas."""

from shared.messaging.events.schemas import (
    CreditCheckedEvent,
    DomainEvent,
    InventoryCheckedEvent,
    InventoryReservedEvent,
    NotificationSentEvent,
    OrderCancelledEvent,
    OrderCreatedEvent,
    OrderUpdatedEvent,
    PaymentCompletedEvent,
    PromotionAppliedEvent,
    ShipmentCreatedEvent,
)

__all__ = [
    "CreditCheckedEvent",
    "DomainEvent",
    "InventoryCheckedEvent",
    "InventoryReservedEvent",
    "NotificationSentEvent",
    "OrderCancelledEvent",
    "OrderCreatedEvent",
    "OrderUpdatedEvent",
    "PaymentCompletedEvent",
    "PromotionAppliedEvent",
    "ShipmentCreatedEvent",
]
