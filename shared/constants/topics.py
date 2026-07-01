from __future__ import annotations

ORDER_CREATED = "order.created"
ORDER_UPDATED = "order.updated"
ORDER_CANCELLED = "order.cancelled"
INVENTORY_CHECKED = "inventory.checked"
INVENTORY_RESERVED = "inventory.reserved"
PROMOTION_APPLIED = "promotion.applied"
CREDIT_CHECKED = "credit.checked"
PAYMENT_COMPLETED = "payment.completed"
SHIPMENT_CREATED = "shipment.created"
NOTIFICATION_SENT = "notification.sent"

ALL_TOPICS: frozenset[str] = frozenset(
    {
        ORDER_CREATED,
        ORDER_UPDATED,
        ORDER_CANCELLED,
        INVENTORY_CHECKED,
        INVENTORY_RESERVED,
        PROMOTION_APPLIED,
        CREDIT_CHECKED,
        PAYMENT_COMPLETED,
        SHIPMENT_CREATED,
        NOTIFICATION_SENT,
    }
)
