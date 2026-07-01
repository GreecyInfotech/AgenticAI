from __future__ import annotations

import pytest

from ai_platform.agents.knowledge_agent.agent import KnowledgeAgent
from ai_platform.agents.knowledge_agent.schemas import KnowledgeAgentInput


@pytest.mark.asyncio
async def test_knowledge_agent_run() -> None:
    agent = KnowledgeAgent()
    result = await agent.run(
        KnowledgeAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "knowledge_agent"
    assert result.confidence > 0
