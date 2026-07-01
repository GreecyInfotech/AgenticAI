from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ai_platform.config.dependencies import get_inventory_repository
from shared.messaging import InventoryCheckedEvent, publish
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.get("/inventory/{sku}")
async def get_inventory(
    sku: str,
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> dict:
    repo = get_inventory_repository()
    item = await repo.get_by_sku(sku)
    event = InventoryCheckedEvent.create(sku=sku, available=item["available"])
    await publish(event.event_type, event)
    return item
