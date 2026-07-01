from __future__ import annotations

from ai_platform.agents.knowledge_agent.prompt import build_promptfrom ai_platform.agents.knowledge_agent.schemas import KnowledgeAgentInput, KnowledgeAgentOutput
from ai_platform.agents.knowledge_agent.tools import get_tools
from ai_platform.llm.factory import get_llm
from ai_platform.rag.retriever.retriever import KnowledgeRetriever
from ai_platform.rag.schemas import RetrievalRequest
from shared.logging import get_logger

logger = get_logger(__name__)


class KnowledgeAgent:
    """Knowledge base and FAQ lookup with RAG retrieval."""

    name = "knowledge_agent"

    def __init__(self) -> None:
        self._retriever = KnowledgeRetriever()

    async def run(self, input_data: KnowledgeAgentInput) -> KnowledgeAgentOutput:
        rag_context = input_data.context.get("rag_context", "")
        if not rag_context:
            response = await self._retriever.retrieve(RetrievalRequest(query=input_data.message, top_k=3))
            rag_context = "\n".join(f"[doc:{c.id}] {c.content}" for c in response.chunks)

        enriched = KnowledgeAgentInput(
            session_id=input_data.session_id,
            customer_id=input_data.customer_id,
            message=input_data.message,
            context={**input_data.context, "rag_context": rag_context},
        )

        llm = get_llm()
        prompt = build_prompt(enriched)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        logger.info("knowledge_agent_completed", customer_id=input_data.customer_id, chunks_used=rag_context.count("[doc:"))
        return KnowledgeAgentOutput(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={"rag_context": rag_context, "input": input_data.model_dump()},
        )
