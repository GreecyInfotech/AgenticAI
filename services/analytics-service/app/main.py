from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from shared.security import CurrentUser, require_permission
from shared.service import create_service_app

app = create_service_app(title="analytics-service", description="Analytics and reporting microservice")


@app.get("/api/v1/analytics/summary", tags=["analytics"])
async def get_summary(
    _user: Annotated[CurrentUser, Depends(require_permission("analytics:read"))],
) -> dict:
    return {
        "total_orders": 1284,
        "revenue_mtd": 458920.50,
        "top_skus": [{"sku": "SKU-001", "units": 420}, {"sku": "SKU-12345", "units": 310}],
    }
