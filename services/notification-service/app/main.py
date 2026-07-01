from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from shared.messaging import NotificationSentEvent, publish
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app

app = create_service_app(title="notification-service", description="Email and SMS notifications microservice")


class SendNotificationRequest(BaseModel):
    channel: str
    recipient: str
    template: str
    data: dict = {}


@app.post("/api/v1/notifications/send", status_code=202, tags=["notifications"])
async def send_notification(
    body: SendNotificationRequest,
    _user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
) -> dict:
    event = NotificationSentEvent.create(body.channel, body.recipient, body.template)
    await publish(event.event_type, event)
    return {"status": "queued", "channel": body.channel, "recipient": body.recipient}
