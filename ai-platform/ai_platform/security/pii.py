from __future__ import annotations

import re

PII_PATTERNS = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    (re.compile(r"\b\d{16}\b"), "[CARD]"),
    (re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b"), "[EMAIL]"),
]


def mask_pii(text: str) -> str:
    for pattern, replacement in PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text
