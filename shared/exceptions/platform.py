from __future__ import annotations

from typing import Any


class PlatformError(Exception):
    """Base exception for all platform errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        error_type: str = "platform-error",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.details = details or {}


class NotFoundError(PlatformError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            f"{resource} '{identifier}' not found",
            status_code=404,
            error_type="not-found",
            details={"resource": resource, "identifier": identifier},
        )


class ValidationError(PlatformError):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message,
            status_code=422,
            error_type="validation-error",
            details=details,
        )


class UnauthorizedError(PlatformError):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message, status_code=401, error_type="unauthorized")


class ForbiddenError(PlatformError):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message, status_code=403, error_type="forbidden")


class ConflictError(PlatformError):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=409, error_type="conflict", details=details)


class IdempotencyConflictError(ConflictError):
    def __init__(self, idempotency_key: str) -> None:
        super().__init__(
            "Request with this Idempotency-Key is already being processed",
            details={"idempotency_key": idempotency_key},
        )


class ServiceUnavailableError(PlatformError):
    def __init__(self, service: str, message: str = "Service unavailable") -> None:
        super().__init__(
            message,
            status_code=503,
            error_type="service-unavailable",
            details={"service": service},
        )
