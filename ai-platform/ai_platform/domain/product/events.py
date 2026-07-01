from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def product_event(event_type: str, payload: dict) -> dict:
    return {
        "event_id": str(uuid4()),
        "domain": "product",
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
