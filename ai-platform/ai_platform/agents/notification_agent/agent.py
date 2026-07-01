from __future__ import annotations

from ai_platform.agents.notification_agent.prompt import build_prompt
from ai_platform.agents.notification_agent.schemas import NotificationAgentInput, NotificationAgentOutput
from ai_platform.agents.notification_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class NotificationAgent:
    """Email and SMS notifications."""

    name = "notification_agent"

    async def run(self, input_data: NotificationAgentInput) -> NotificationAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return NotificationAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
