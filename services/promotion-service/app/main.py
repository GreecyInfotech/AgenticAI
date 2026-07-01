from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from shared.messaging import PromotionAppliedEvent, publish
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app

app = create_service_app(title="promotion-service", description="Promotions and campaigns microservice")

_PROMOS: dict[str, float] = {"SAVE10": 0.10, "SAVE20": 0.20}


class ApplyPromotionRequest(BaseModel):
    order_id: str
    promotion_code: str
    order_total: float


@app.post("/api/v1/promotions/apply", tags=["promotions"])
async def apply_promotion(
    body: ApplyPromotionRequest,
    _user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
) -> dict:
    from shared.exceptions import NotFoundError

    if body.promotion_code not in _PROMOS:
        raise NotFoundError("promotion", body.promotion_code)
    discount_rate = _PROMOS[body.promotion_code]
    discount = body.order_total * discount_rate
    event = PromotionAppliedEvent.create(body.order_id, body.promotion_code, discount)
    await publish(event.event_type, event)
    return {"order_id": body.order_id, "promotion_code": body.promotion_code, "discount": discount}
