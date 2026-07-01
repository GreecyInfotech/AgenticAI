from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from ai_platform.api.v1 import auth, conversation, customer, health, inventory, metrics, orders, products
from ai_platform.app.lifespan import lifespan
from ai_platform.app.middleware import AuditLogMiddleware, RequestIdMiddleware
from ai_platform.config.settings import get_settings
from shared.common.problem_details import platform_error_handler, problem_response
from shared.exceptions import PlatformError
from shared.logging import configure_logging
from shared.telemetry import instrument_fastapi


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="AI Distributor Ordering Platform",
        version="0.1.0",
        description="LangGraph-powered distributor ordering with RAG and multi-agent orchestration",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(AuditLogMiddleware)

    @app.exception_handler(PlatformError)
    async def _platform_error(request: Request, exc: PlatformError):
        return platform_error_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError):
        return problem_response(
            request=request,
            status=422,
            title="Validation Error",
            detail="Request validation failed",
            error_type="https://api.distributor.platform/errors/validation-error",
            errors={"errors": exc.errors()},
        )

    prefix = "/api/v1"
    app.include_router(health.router, prefix=prefix, tags=["health"])
    app.include_router(metrics.router, prefix=prefix, tags=["metrics"])
    app.include_router(auth.router, prefix=prefix, tags=["auth"])
    app.include_router(conversation.router, prefix=prefix, tags=["conversation"])
    app.include_router(orders.router, prefix=prefix, tags=["orders"])
    app.include_router(inventory.router, prefix=prefix, tags=["inventory"])
    app.include_router(products.router, prefix=prefix, tags=["products"])
    app.include_router(customer.router, prefix=prefix, tags=["customer"])

    instrument_fastapi(app, "ai-platform")
    return app
