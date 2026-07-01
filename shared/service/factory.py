from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from shared.common.problem_details import platform_error_handler, problem_response
from shared.config.settings import get_base_settings
from shared.exceptions import PlatformError
from shared.logging import configure_logging, get_logger
from shared.messaging import close_kafka_producer, init_kafka_producer
from shared.telemetry import instrument_fastapi

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        import uuid

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


@asynccontextmanager
async def default_lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_base_settings()
    configure_logging(settings.log_level)
    logger.info("service_starting", service=app.title, env=settings.app_env)
    await init_kafka_producer()
    app.state.ready = True
    yield
    app.state.ready = False
    await close_kafka_producer()
    logger.info("service_stopped", service=app.title)


def create_service_app(
    *,
    title: str,
    version: str = "0.1.0",
    description: str = "",
    lifespan: Callable[[FastAPI], Any] | None = None,
    include_metrics: bool = True,
) -> FastAPI:
    settings = get_base_settings()
    app = FastAPI(
        title=title,
        version=version,
        description=description,
        lifespan=lifespan or default_lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)

    @app.exception_handler(PlatformError)
    async def _platform_error(request: Request, exc: PlatformError) -> Response:
        return platform_error_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError) -> Response:
        return problem_response(
            request=request,
            status=422,
            title="Validation Error",
            detail="Request validation failed",
            error_type="https://api.distributor.platform/errors/validation-error",
            errors={"errors": exc.errors()},
        )

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "UP", "service": title}

    @app.get("/ready", tags=["health"])
    async def ready(request: Request) -> dict[str, str]:
        if not getattr(request.app.state, "ready", False):
            return problem_response(
                request=request,
                status=503,
                title="Not Ready",
                detail="Service is starting",
                error_type="https://api.distributor.platform/errors/not-ready",
            )  # type: ignore[return-value]
        return {"status": "READY", "service": title}

    if include_metrics:

        @app.get("/metrics", tags=["metrics"])
        async def metrics() -> Response:
            return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    instrument_fastapi(app, title)
    return app
