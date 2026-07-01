from __future__ import annotations

from ai_platform.agents.supervisor_agent.prompt import build_prompt
from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentInput, SupervisorAgentOutput
from ai_platform.agents.supervisor_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class SupervisorAgent:
    """Routes requests to specialist agents."""

    name = "supervisor_agent"

    async def run(self, input_data: SupervisorAgentInput) -> SupervisorAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return SupervisorAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
