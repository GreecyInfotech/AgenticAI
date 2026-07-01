from __future__ import annotations

from ai_platform.llm.guardrails import validate_output

def apply_guardrails(text: str) -> str:
    return validate_output(text)
