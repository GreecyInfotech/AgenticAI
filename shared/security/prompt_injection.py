from __future__ import annotations

INJECTION_PATTERNS = [
    "ignore previous",
    "system prompt",
    "you are now",
    "disregard",
    "jailbreak",
    "override instructions",
]


def is_prompt_injection(text: str) -> bool:
    lower = text.lower()
    return any(pattern in lower for pattern in INJECTION_PATTERNS)
