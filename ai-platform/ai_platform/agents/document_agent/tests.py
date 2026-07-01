from __future__ import annotations

import pytest

from ai_platform.agents.document_agent.agent import DocumentAgent
from ai_platform.agents.document_agent.schemas import DocumentAgentInput


@pytest.mark.asyncio
async def test_document_agent_run() -> None:
    agent = DocumentAgent()
    result = await agent.run(
        DocumentAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "document_agent"
    assert result.confidence > 0
