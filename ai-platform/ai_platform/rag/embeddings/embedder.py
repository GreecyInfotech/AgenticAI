from __future__ import annotations

async def embed_text(text: str) -> list[float]:
    return [float(ord(c) % 100) / 100.0 for c in text[:32]]
