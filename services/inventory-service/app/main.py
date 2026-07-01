from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from shared.messaging import InventoryCheckedEvent, publish
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app

app = create_service_app(title="inventory-service", description="Stock and availability microservice")

_inventory: dict[str, dict] = {
    "SKU-001": {"sku": "SKU-001", "available": 500, "warehouse": "WH-01"},
    "SKU-12345": {"sku": "SKU-12345", "available": 120, "warehouse": "WH-01"},
}


class ReserveRequest(BaseModel):
    quantity: int
    order_id: str


@app.get("/api/v1/inventory/{sku}", tags=["inventory"])
async def get_inventory(
    sku: str,
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> dict:
    from shared.exceptions import NotFoundError

    if sku not in _inventory:
        raise NotFoundError("inventory", sku)
    item = _inventory[sku]
    event = InventoryCheckedEvent.create(sku=sku, available=item["available"])
    await publish(event.event_type, event)
    return item


@app.post("/api/v1/inventory/{sku}/reserve", tags=["inventory"])
async def reserve_inventory(
    sku: str,
    body: ReserveRequest,
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> dict:
    from shared.exceptions import NotFoundError, ValidationError
    from shared.messaging import InventoryReservedEvent

    if sku not in _inventory:
        raise NotFoundError("inventory", sku)
    if _inventory[sku]["available"] < body.quantity:
        raise ValidationError("Insufficient stock", details={"available": _inventory[sku]["available"]})
    _inventory[sku]["available"] -= body.quantity
    event = InventoryReservedEvent.create(sku=sku, quantity=body.quantity, order_id=body.order_id)
    await publish(event.event_type, event)
    return {"sku": sku, "reserved": body.quantity, "remaining": _inventory[sku]["available"]}
