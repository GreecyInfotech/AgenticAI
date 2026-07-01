"""Generate agent module files."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "ai-platform" / "ai_platform" / "agents"

AGENTS: dict[str, str] = {
    "customer_agent": "Customer profile and account management",
    "inventory_agent": "Stock levels and availability checks",
    "pricing_agent": "Price quotes and discount rules",
    "promotion_agent": "Promotions and campaign eligibility",
    "credit_agent": "Credit limits and payment terms",
    "recommendation_agent": "Product recommendations",
    "order_agent": "Order placement and validation",
    "shipment_agent": "Shipment tracking and logistics",
    "payment_agent": "Payment processing and status",
    "notification_agent": "Email and SMS notifications",
    "analytics_agent": "Order and sales analytics",
    "document_agent": "Invoice and document generation",
    "knowledge_agent": "Knowledge base and FAQ lookup",
    "supervisor_agent": "Routes requests to specialist agents",
}


def to_class(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


for agent_name, description in AGENTS.items():
    cls = to_class(agent_name)
    d = ROOT / agent_name
    d.mkdir(parents=True, exist_ok=True)

    (d / "__init__.py").write_text(f'"""{cls} module."""\n', encoding="utf-8")

    (d / "schemas.py").write_text(
        f'''from __future__ import annotations

from pydantic import BaseModel, Field


class {cls}Input(BaseModel):
    session_id: str
    customer_id: str
    message: str
    context: dict = Field(default_factory=dict)


class {cls}Output(BaseModel):
    agent: str
    message: str
    confidence: float = Field(ge=0.0, le=1.0)
    data: dict = Field(default_factory=dict)
    requires_escalation: bool = False
''',
        encoding="utf-8",
    )

    (d / "prompt.py").write_text(
        f'''from __future__ import annotations

from ai_platform.agents.{agent_name}.schemas import {cls}Input


def build_prompt(input_data: {cls}Input) -> str:
    return (
        "You are the {agent_name.replace("_", " ")} for a distributor ordering platform.\\n"
        f"Customer: {{input_data.customer_id}}\\n"
        f"Request: {{input_data.message}}\\n"
        "Respond with actionable distributor ordering guidance."
    )
''',
        encoding="utf-8",
    )

    (d / "tools.py").write_text(
        '''from __future__ import annotations

from typing import Any


def get_tools() -> list[dict[str, Any]]:
    return []
''',
        encoding="utf-8",
    )

    (d / "state.py").write_text(
        f'''from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.{agent_name}.schemas import {cls}Output


class {cls}State(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: {cls}Output | None
    next_agent: str | None
''',
        encoding="utf-8",
    )

    (d / "memory.py").write_text(
        f'''from __future__ import annotations

from ai_platform.memory.session_memory import SessionMemory


class {cls}Memory:
    def __init__(self, session_id: str) -> None:
        self._memory = SessionMemory(session_id)

    async def load(self) -> list[dict]:
        return await self._memory.get_messages()

    async def save(self, role: str, content: str) -> None:
        await self._memory.add_message(role, content)
''',
        encoding="utf-8",
    )

    (d / "agent.py").write_text(
        f'''from __future__ import annotations

from ai_platform.agents.{agent_name}.prompt import build_prompt
from ai_platform.agents.{agent_name}.schemas import {cls}Input, {cls}Output
from ai_platform.agents.{agent_name}.tools import get_tools
from ai_platform.llm.factory import get_llm


class {cls}:
    """{description}."""

    name = "{agent_name}"

    async def run(self, input_data: {cls}Input) -> {cls}Output:
        llm = get_llm()
        prompt = build_prompt(input_data)
        tools = get_tools()
        response = await llm.ainvoke(prompt, tools=tools)
        return {cls}Output(
            agent=self.name,
            message=str(response),
            confidence=0.85,
            data={{"input": input_data.model_dump()}},
        )
''',
        encoding="utf-8",
    )

    (d / "tests.py").write_text(
        f'''from __future__ import annotations

import pytest

from ai_platform.agents.{agent_name}.agent import {cls}
from ai_platform.agents.{agent_name}.schemas import {cls}Input


@pytest.mark.asyncio
async def test_{agent_name}_run() -> None:
    agent = {cls}()
    result = await agent.run(
        {cls}Input(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "{agent_name}"
    assert result.confidence > 0
''',
        encoding="utf-8",
    )

print(f"Generated {len(AGENTS)} agents")
