from __future__ import annotations

from ai_platform.agents.order_agent.prompt import build_prompt
from ai_platform.agents.order_agent.schemas import OrderAgentInput, OrderAgentOutput
from ai_platform.agents.order_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class OrderAgent:
    """Order placement and validation."""

    name = "order_agent"

    async def run(self, input_data: OrderAgentInput) -> OrderAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return OrderAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
