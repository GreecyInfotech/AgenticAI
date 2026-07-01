from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from shared.messaging import ShipmentCreatedEvent, publish
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app
from shared.utils.ids import generate_id

app = create_service_app(title="shipment-service", description="Shipment and logistics microservice")


class CreateShipmentRequest(BaseModel):
    order_id: str
    carrier: str = "FedEx"


@app.post("/api/v1/shipments", status_code=201, tags=["shipments"])
async def create_shipment(
    body: CreateShipmentRequest,
    _user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
) -> dict:
    shipment_id = generate_id("SHP")
    result = {"shipment_id": shipment_id, "order_id": body.order_id, "carrier": body.carrier, "status": "created"}
    event = ShipmentCreatedEvent.create(body.order_id, shipment_id, body.carrier)
    await publish(event.event_type, event)
    return result


@app.get("/api/v1/shipments/{shipment_id}", tags=["shipments"])
async def track_shipment(
    shipment_id: str,
    _user: Annotated[CurrentUser, Depends(require_permission("orders:read"))],
) -> dict:
    return {"shipment_id": shipment_id, "status": "in_transit", "eta": "2026-07-05"}
