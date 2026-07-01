from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ai_platform.application.dto.inventory_dto import InventoryResponseDTO
from ai_platform.application.use_cases.get_inventory import GetInventoryUseCase
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.get("/inventory/{sku}", response_model=InventoryResponseDTO)
async def get_inventory(
    sku: str,
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> InventoryResponseDTO:
    return await GetInventoryUseCase().execute(sku)
