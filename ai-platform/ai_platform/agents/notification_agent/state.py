from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.notification_agent.schemas import NotificationAgentOutput


class NotificationAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: NotificationAgentOutput | None
    next_agent: str | None
