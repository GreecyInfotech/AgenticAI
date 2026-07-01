from __future__ import annotations

from ai_platform.agents.document_agent.prompt import build_prompt
from ai_platform.agents.document_agent.schemas import DocumentAgentInput, DocumentAgentOutput
from ai_platform.agents.document_agent.tools import get_tools
from ai_platform.llm.factory import get_llm


class DocumentAgent:
    """Invoice and document generation."""

    name = "document_agent"

    async def run(self, input_data: DocumentAgentInput) -> DocumentAgentOutput:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return DocumentAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"input": input_data.model_dump()},
        )
