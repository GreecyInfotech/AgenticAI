from __future__ import annotations

from ai_platform.agents.recommendation_agent.prompt import build_prompt
from ai_platform.agents.recommendation_agent.schemas import RecommendationAgentInput, RecommendationAgentOutput
from ai_platform.agents.recommendation_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class RecommendationAgent:
    """Product recommendations."""

    name = "recommendation_agent"

    async def run(self, input_data: RecommendationAgentInput) -> RecommendationAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return RecommendationAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
