from __future__ import annotations

import re
from typing import Any

PII_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    (re.compile(r"\b\d{16}\b"), "[CARD]"),
    (re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b"), "[EMAIL]"),
    (re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"), "[PHONE]"),
]


def mask_pii(text: str) -> str:
    for pattern, replacement in PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def mask_pii_in_dict(value: Any) -> Any:
    if isinstance(value, str):
        return mask_pii(value)
    if isinstance(value, dict):
        return {k: mask_pii_in_dict(v) for k, v in value.items()}
    if isinstance(value, list):
        return [mask_pii_in_dict(item) for item in value]
    return value
