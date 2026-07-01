from __future__ import annotations

from shared.exceptions import ValidationError
from shared.security.prompt_injection import is_prompt_injection


def validate_input(text: str) -> str:
    if not text or not text.strip():
        raise ValidationError("Prompt cannot be empty")
    if is_prompt_injection(text):
        raise ValidationError("Message rejected: potential prompt injection detected")
    return text


def validate_output(text: str) -> str:
    if is_prompt_injection(text):
        return "I cannot process that request."
    return text
