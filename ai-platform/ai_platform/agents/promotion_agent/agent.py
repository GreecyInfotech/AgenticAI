from __future__ import annotations

from ai_platform.agents.promotion_agent.prompt import build_prompt
from ai_platform.agents.promotion_agent.schemas import PromotionAgentInput, PromotionAgentOutput
from ai_platform.agents.promotion_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class PromotionAgent:
    """Promotions and campaign eligibility."""

    name = "promotion_agent"

    async def run(self, input_data: PromotionAgentInput) -> PromotionAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return PromotionAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
