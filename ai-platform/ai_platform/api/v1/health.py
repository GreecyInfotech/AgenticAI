from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ai_platform.infrastructure.crm import check_crm_health
from ai_platform.infrastructure.database import check_db_health
from ai_platform.infrastructure.email import check_email_health
from ai_platform.infrastructure.kafka import check_kafka_health
from ai_platform.infrastructure.qdrant_client import check_qdrant_health
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
    dependencies = {
        "postgres": await check_db_health(),
        "redis": await check_redis_health(),
        "qdrant": await check_qdrant_health(),
        "kafka": await check_kafka_health(),
        "email": await check_email_health(),
        "crm": await check_crm_health(),
    }
    critical = [dependencies["postgres"], dependencies["redis"]]
    degraded = any(dep.get("status") == "DOWN" for dep in critical)
    return {
        "status": "DEGRADED" if degraded else "READY",
        "service": "ai-platform",
        "dependencies": dependencies,
    }
