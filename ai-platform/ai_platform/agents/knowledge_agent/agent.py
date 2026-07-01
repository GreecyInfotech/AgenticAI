from __future__ import annotations

from ai_platform.agents.knowledge_agent.prompt import build_prompt
from ai_platform.agents.knowledge_agent.schemas import KnowledgeAgentInput, KnowledgeAgentOutput
from ai_platform.agents.knowledge_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class KnowledgeAgent:
    """Knowledge base and FAQ lookup."""

    name = "knowledge_agent"

    async def run(self, input_data: KnowledgeAgentInput) -> KnowledgeAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return KnowledgeAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
