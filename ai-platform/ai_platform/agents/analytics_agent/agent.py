from __future__ import annotations

from ai_platform.agents.analytics_agent.prompt import build_prompt
from ai_platform.agents.analytics_agent.schemas import AnalyticsAgentInput, AnalyticsAgentOutput
from ai_platform.agents.analytics_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class AnalyticsAgent:
    """Order and sales analytics."""

    name = "analytics_agent"

    async def run(self, input_data: AnalyticsAgentInput) -> AnalyticsAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return AnalyticsAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
