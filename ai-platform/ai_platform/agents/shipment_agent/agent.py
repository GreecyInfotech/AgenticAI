from __future__ import annotations

from ai_platform.agents.shipment_agent.prompt import build_prompt
from ai_platform.agents.shipment_agent.schemas import ShipmentAgentInput, ShipmentAgentOutput
from ai_platform.agents.shipment_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class ShipmentAgent:
    """Shipment tracking and logistics."""

    name = "shipment_agent"

    async def run(self, input_data: ShipmentAgentInput) -> ShipmentAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return ShipmentAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
