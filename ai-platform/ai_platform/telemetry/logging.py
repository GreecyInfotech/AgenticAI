"""Delegates to shared.logging — use shared.logging in new code."""

from shared.logging import configure_logging, get_logger

__all__ = ["configure_logging", "get_logger"]
