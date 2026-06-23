"""LangGraph agent implementation for incident-agent."""

import json
import uuid
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from smart_port_common.config import get_settings
from smart_port_common.logging import get_logger

from config import AgentSettings

logger = get_logger(__name__)
settings = AgentSettings()

SYSTEM_PROMPT = """You are the Smart Port Incident Agent.
You help port operators with incident-related tasks including:
- detect incident
- triage incident
- escalate
- generate report

Always provide actionable, data-driven recommendations.
Cite specific tool results when available. Be concise and professional."""


@tool
def detect_incident(input_data: str) -> str:
    """Execute detect incident for incident operations."""
    return json.dumps({"tool": "detect_incident", "domain": "incident", "result": "success", "data": input_data})

@tool
def triage_incident(input_data: str) -> str:
    """Execute triage incident for incident operations."""
    return json.dumps({"tool": "triage_incident", "domain": "incident", "result": "success", "data": input_data})

@tool
def escalate(input_data: str) -> str:
    """Execute escalate for incident operations."""
    return json.dumps({"tool": "escalate", "domain": "incident", "result": "success", "data": input_data})

@tool
def generate_report(input_data: str) -> str:
    """Execute generate report for incident operations."""
    return json.dumps({"tool": "generate_report", "domain": "incident", "result": "success", "data": input_data})


def _get_llm() -> ChatOpenAI:
    cfg = get_settings()
    if cfg.azure_openai_endpoint:
        return ChatOpenAI(
            azure_endpoint=cfg.azure_openai_endpoint,
            api_key=cfg.azure_openai_api_key,
            azure_deployment=cfg.azure_openai_deployment,
            api_version="2024-02-01",
        )
    return ChatOpenAI(model="gpt-4o", api_key=cfg.openai_api_key or "not-set")


async def run_agent(
    query: str,
    context: dict[str, Any] | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    context = context or {}
    session_id = session_id or str(uuid.uuid4())

    llm = _get_llm()
    tools = [detect_incident, triage_incident, escalate, generate_report]
    agent = create_react_agent(llm, tools)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context: {json.dumps(context)}\n\nQuery: {query}"),
    ]

    logger.info("agent_invocation", session_id=session_id, query=query[:100])
    result = await agent.ainvoke({"messages": messages})

    final_message = result["messages"][-1].content
    tools_used = [
        tc.get("name", "") for msg in result["messages"]
        if hasattr(msg, "tool_calls") and msg.tool_calls
        for tc in (msg.tool_calls or [])
    ]

    return {
        "answer": final_message,
        "tools_used": tools_used,
        "confidence": 0.85,
        "session_id": session_id,
        "metadata": {"domain": "incident", "agent": "incident-agent"},
    }
