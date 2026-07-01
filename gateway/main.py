from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from shared.common.problem_details import platform_error_handler
from shared.config.settings import get_base_settings
from shared.exceptions import PlatformError, ServiceUnavailableError, UnauthorizedError
from shared.logging import get_logger
from shared.security import decode_token
from shared.service import create_service_app

logger = get_logger(__name__)

AI_PLATFORM_URL = os.getenv("AI_PLATFORM_URL", "http://localhost:8000")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8001")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://localhost:8002")
CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8003")

ROUTE_MAP: dict[str, str] = {
    "/api/v1/conversation": AI_PLATFORM_URL,
    "/api/v1/orders": ORDER_SERVICE_URL,
    "/api/v1/inventory": INVENTORY_SERVICE_URL,
    "/api/v1/products": AI_PLATFORM_URL,
    "/api/v1/customers": CUSTOMER_SERVICE_URL,
    "/api/v1/auth": AI_PLATFORM_URL,
    "/api/v1/health": AI_PLATFORM_URL,
    "/api/v1/metrics": AI_PLATFORM_URL,
}

PUBLIC_PATHS = {"/health", "/ready", "/metrics", "/api/v1/health", "/api/v1/auth/token"}


def _resolve_upstream(path: str) -> str:
    for prefix, base_url in ROUTE_MAP.items():
        if path.startswith(prefix):
            return base_url
    return AI_PLATFORM_URL


def _validate_auth(request: Request) -> None:
    if request.url.path in PUBLIC_PATHS:
        return
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise UnauthorizedError()
    decode_token(auth.removeprefix("Bearer ").strip())


app = create_service_app(
    title="API Gateway",
    description="Unified entry point for AI Distributor Ordering Platform",
)


@app.middleware("http")
async def gateway_proxy(request: Request, call_next) -> Response:
    if request.url.path in {"/health", "/ready", "/metrics"}:
        return await call_next(request)

    try:
        _validate_auth(request)
    except PlatformError as exc:
        return platform_error_handler(request, exc)

    upstream_base = _resolve_upstream(request.url.path)
    upstream_url = f"{upstream_base}{request.url.path}"
    if request.url.query:
        upstream_url = f"{upstream_url}?{request.url.query}"

    headers = {k: v for k, v in request.headers.items() if k.lower() not in {"host", "content-length"}}
    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream_response = await client.request(
                request.method,
                upstream_url,
                headers=headers,
                content=body,
            )
    except httpx.RequestError as exc:
        logger.error("upstream_unavailable", url=upstream_url, error=str(exc))
        raise ServiceUnavailableError("gateway", f"Upstream unavailable: {upstream_url}") from exc

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=dict(upstream_response.headers),
        media_type=upstream_response.headers.get("content-type"),
    )