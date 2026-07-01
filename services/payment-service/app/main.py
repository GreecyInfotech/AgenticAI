from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header
from pydantic import BaseModel

from shared.common.idempotency import idempotency_store
from shared.constants.status import PAYMENT_STATUS_COMPLETED
from shared.messaging import PaymentCompletedEvent, publish
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app
from shared.utils.ids import generate_id

app = create_service_app(title="payment-service", description="Payment processing microservice")


class PaymentRequest(BaseModel):
    order_id: str
    amount: float
    method: str = "card"


@app.post("/api/v1/payments", status_code=201, tags=["payments"])
async def process_payment(
    body: PaymentRequest,
    user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> dict:
    if idempotency_key:
        cached = await idempotency_store.get(idempotency_key)
        if cached and cached.get("status") == "completed":
            return cached["response"]
        await idempotency_store.set(idempotency_key, {"status": "processing"})

    payment_id = generate_id("PAY")
    result = {
        "payment_id": payment_id,
        "order_id": body.order_id,
        "amount": body.amount,
        "status": PAYMENT_STATUS_COMPLETED,
        "method": body.method,
    }
    event = PaymentCompletedEvent.create(body.order_id, body.amount, payment_id)
    await publish(event.event_type, event)
    if idempotency_key:
        await idempotency_store.complete(idempotency_key, result)
    return result
