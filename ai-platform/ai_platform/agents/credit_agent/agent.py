from __future__ import annotations

from ai_platform.agents.credit_agent.prompt import build_prompt
from ai_platform.agents.credit_agent.schemas import CreditAgentInput, CreditAgentOutput
from ai_platform.agents.credit_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class CreditAgent:
    """Credit limits and payment terms."""

    name = "credit_agent"

    async def run(self, input_data: CreditAgentInput) -> CreditAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return CreditAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
