from __future__ import annotations

from ai_platform.agents.customer_agent.prompt import build_prompt
from ai_platform.agents.customer_agent.schemas import CustomerAgentInput, CustomerAgentOutput
from ai_platform.agents.customer_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class CustomerAgent:
    """Customer profile and account management."""

    name = "customer_agent"

    async def run(self, input_data: CustomerAgentInput) -> CustomerAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return CustomerAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
