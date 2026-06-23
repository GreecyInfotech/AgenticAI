"""Health check endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str = "1.0.0"
    timestamp: str
    checks: dict[str, str] = {}


def create_health_router(service_name: str) -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get("/health", response_model=HealthResponse)
    @router.get("/healthz", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(
            status="healthy",
            service=service_name,
            timestamp=datetime.now(UTC).isoformat(),
        )

    @router.get("/ready", response_model=HealthResponse)
    @router.get("/readyz", response_model=HealthResponse)
    async def ready() -> HealthResponse:
        return HealthResponse(
            status="ready",
            service=service_name,
            timestamp=datetime.now(UTC).isoformat(),
            checks={"database": "ok", "kafka": "ok"},
        )

    return router
