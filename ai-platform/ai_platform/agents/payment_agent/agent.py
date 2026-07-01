from __future__ import annotations

from ai_platform.agents.payment_agent.prompt import build_prompt
from ai_platform.agents.payment_agent.schemas import PaymentAgentInput, PaymentAgentOutput
from ai_platform.agents.payment_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class PaymentAgent:
    """Payment processing and status."""

    name = "payment_agent"

    async def run(self, input_data: PaymentAgentInput) -> PaymentAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return PaymentAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
