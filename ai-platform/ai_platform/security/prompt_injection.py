from __future__ import annotations

INJECTION_PATTERNS = ["ignore previous", "system prompt", "you are now", "disregard"]


def is_prompt_injection(text: str) -> bool:
    lower = text.lower()
    return any(p in lower for p in INJECTION_PATTERNS)
