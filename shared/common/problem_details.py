from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from shared.exceptions import PlatformError


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None
    errors: dict[str, Any] | None = None


def problem_response(
    *,
    request: Request,
    status: int,
    title: str,
    detail: str,
    error_type: str = "about:blank",
    errors: dict[str, Any] | None = None,
) -> JSONResponse:
    body = ProblemDetail(
        type=error_type,
        title=title,
        status=status,
        detail=detail,
        instance=str(request.url),
        errors=errors,
    )
    return JSONResponse(status_code=status, content=body.model_dump(exclude_none=True))


def platform_error_handler(request: Request, exc: PlatformError) -> JSONResponse:
    return problem_response(
        request=request,
        status=exc.status_code,
        title=exc.error_type.replace("-", " ").title(),
        detail=exc.message,
        error_type=f"https://api.distributor.platform/errors/{exc.error_type}",
        errors=exc.details or None,
    )
