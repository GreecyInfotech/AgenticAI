from __future__ import annotations

import logging
import sys

import structlog

from shared.security.pii import mask_pii_in_dict


def _mask_pii_processor(
    _logger: logging.Logger,
    _method: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    for key in ("message", "msg", "error", "prompt", "response"):
        if key in event_dict and isinstance(event_dict[key], str):
            event_dict[key] = mask_pii_in_dict(event_dict[key])  # type: ignore[arg-type]
    for key in ("payload", "context", "details"):
        if key in event_dict and isinstance(event_dict[key], dict):
            event_dict[key] = mask_pii_in_dict(event_dict[key])
    return event_dict


def configure_logging(level: str = "INFO") -> None:
    """Configure structlog with PII masking for all services."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _mask_pii_processor,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
