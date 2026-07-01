from __future__ import annotations

from ai_platform.agents.notification_agent.schemas import NotificationAgentInput


def build_prompt(input_data: NotificationAgentInput) -> str:
    return (
        "You are the notification agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
