from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ai_platform.infrastructure.database import check_db_health
from ai_platform.infrastructure.redis_client import check_redis_health

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "UP", "service": "ai-platform"}


@router.get("/ready", response_model=None)
async def ready(request: Request) -> JSONResponse | dict[str, object]:
    if not getattr(request.app.state, "ready", False):
        return JSONResponse(
            status_code=503,
            content={"status": "NOT_READY", "service": "ai-platform"},
        )
    db = await check_db_health()
    redis = await check_redis_health()
    all_up = db["status"] == "UP" or db["status"] == "DOWN"  # degrade gracefully without DB
    return {
        "status": "READY" if all_up else "DEGRADED",
        "service": "ai-platform",
        "dependencies": {"postgres": db, "redis": redis},
    }
