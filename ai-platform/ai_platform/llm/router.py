from __future__ import annotations

from ai_platform.config.settings import get_settings


def get_provider_name() -> str:
    return get_settings().llm_provider
