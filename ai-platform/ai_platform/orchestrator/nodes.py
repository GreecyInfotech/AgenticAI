from __future__ import annotations

import importlib
from typing import Any

from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentInput
from ai_platform.memory.factory import get_session_memory, get_summary_memory
from ai_platform.orchestrator.events import emit_event
from ai_platform.orchestrator.router import parse_supervisor_routing, route
from ai_platform.orchestrator.state import OrchestratorState
from ai_platform.rag.retriever.retriever import KnowledgeRetriever
from ai_platform.rag.schemas import RetrievalRequest
from ai_platform.telemetry.metrics import record_agent_invocation
from ai_platform.telemetry.tracing import agent_span
from shared.logging import get_logger

logger = get_logger(__name__)


async def _load_memory_context(state: OrchestratorState) -> tuple[str, list[dict[str, str]]]:
    memory = get_session_memory(state["session_id"])
    history = await memory.get_messages()
    summary = await get_summary_memory().summarize(
        history,
        session_id=state["session_id"],
        customer_id=state["customer_id"],
    )
    return summary, history


async def _load_rag_context(message: str, target_agent: str) -> str:
    if target_agent != "knowledge_agent":
        return ""
    retriever = KnowledgeRetriever()
    response = await retriever.retrieve(RetrievalRequest(query=message, top_k=3))
    if not response.chunks:
        return ""
    lines = [f"[doc:{chunk.id}] {chunk.content}" for chunk in response.chunks]
    return "\n".join(lines)


async def supervisor_node(state: OrchestratorState) -> dict[str, Any]:
    from ai_platform.agents.supervisor_agent.agent import SupervisorAgent

    memory_summary, history = await _load_memory_context(state)
    supervisor = SupervisorAgent()
    with agent_span("supervisor_agent", state["session_id"]):
        result = await supervisor.run(
            SupervisorAgentInput(
                session_id=state["session_id"],
                customer_id=state["customer_id"],
                message=state["message"],
                context={"memory_summary": memory_summary},
            )
        )
    record_agent_invocation("supervisor_agent", success=True)

    target = route(state, supervisor_message=result.message)
    requires_escalation = False
    parsed = parse_supervisor_routing(result.message)
    if parsed:
        requires_escalation = bool(parsed.get("requires_escalation", False))

    await emit_event("conversation.routed", {"session_id": state["session_id"], "target_agent": target})
    return {
        "target_agent": target,
        "memory_summary": memory_summary,
        "conversation_history": history,
        "requires_escalation": requires_escalation,
        "agent_results": [{"agent": "supervisor_agent", **result.model_dump()}],
    }


async def domain_node(state: OrchestratorState) -> dict[str, Any]:
    target = state.get("target_agent") or "customer_agent"
    rag_context = await _load_rag_context(state["message"], target)

    module = importlib.import_module(f"ai_platform.agents.{target}.agent")
    schemas = importlib.import_module(f"ai_platform.agents.{target}.schemas")
    class_prefix = "".join(part.capitalize() for part in target.split("_"))
    agent_cls = getattr(module, class_prefix)
    input_cls = getattr(schemas, f"{class_prefix}Input")

    agent = agent_cls()
    input_data = input_cls(
        session_id=state["session_id"],
        customer_id=state["customer_id"],
        message=state["message"],
        context={
            "memory_summary": state.get("memory_summary", ""),
            "rag_context": rag_context,
            "conversation_history": state.get("conversation_history", []),
        },
    )

    try:
        with agent_span(target, state["session_id"]):
            result = await agent.run(input_data)
        record_agent_invocation(target, success=True)
    except Exception as exc:
        record_agent_invocation(target, success=False)
        logger.error("domain_agent_failed", agent=target, error=str(exc))
        raise

    memory = get_session_memory(state["session_id"])
    await memory.add_message("user", state["message"])
    await memory.add_message("assistant", result.message)

    results = list(state.get("agent_results", []))
    results.append(result.model_dump())
    await emit_event("conversation.completed", {"session_id": state["session_id"], "agent": target})
    return {
        "agent_results": results,
        "reply": result.message,
        "requires_escalation": result.requires_escalation or state.get("requires_escalation", False),
        "rag_context": rag_context,
    }
