from __future__ import annotations

from ai_platform.security.prompt_injection import is_prompt_injection


def validate_output(text: str) -> str:
    if is_prompt_injection(text):
        return "I cannot process that request."
    return text
