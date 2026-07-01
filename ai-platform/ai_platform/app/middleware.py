from __future__ import annotations

import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from shared.logging import get_logger

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response


class AuditLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, audit_paths: tuple[str, ...] = ("/api/v1/orders", "/api/v1/conversation")) -> None:
        super().__init__(app)
        self._audit_paths = audit_paths

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if any(request.url.path.startswith(path) for path in self._audit_paths):
            logger.info(
                "audit_event",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                request_id=getattr(request.state, "request_id", None),
            )
        return response


def register_middleware(app, middleware_cls: type[BaseHTTPMiddleware], **kwargs) -> None:
    app.add_middleware(middleware_cls, **kwargs)  # type: ignore[arg-type]
