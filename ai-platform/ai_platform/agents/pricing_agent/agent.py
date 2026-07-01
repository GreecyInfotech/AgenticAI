from __future__ import annotations

from ai_platform.agents.pricing_agent.prompt import build_prompt
from ai_platform.agents.pricing_agent.schemas import PricingAgentInput, PricingAgentOutput
from ai_platform.agents.pricing_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class PricingAgent:
    """Price quotes and discount rules."""

    name = "pricing_agent"

    async def run(self, input_data: PricingAgentInput) -> PricingAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return PricingAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
