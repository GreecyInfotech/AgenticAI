from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from shared.messaging import publish


async def emit_event(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    event = {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    await publish(event_type, event)
    return event
