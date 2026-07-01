from __future__ import annotations

from ai_platform.agents.inventory_agent.prompt import build_prompt
from ai_platform.agents.inventory_agent.schemas import InventoryAgentInput, InventoryAgentOutput
from ai_platform.agents.inventory_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class InventoryAgent:
    """Stock levels and availability checks."""

    name = "inventory_agent"

    async def run(self, input_data: InventoryAgentInput) -> InventoryAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return InventoryAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
