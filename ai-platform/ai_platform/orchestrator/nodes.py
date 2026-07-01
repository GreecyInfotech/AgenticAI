from __future__ import annotations

import importlib
from typing import Any

from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentInput
from ai_platform.orchestrator.events import emit_event
from ai_platform.orchestrator.router import route
from ai_platform.orchestrator.state import OrchestratorState


async def supervisor_node(state: OrchestratorState) -> dict[str, Any]:
    from ai_platform.agents.supervisor_agent.agent import SupervisorAgent

    supervisor = SupervisorAgent()
    result = await supervisor.run(
        SupervisorAgentInput(
            session_id=state["session_id"],
            customer_id=state["customer_id"],
            message=state["message"],
        )
    )
    target = route(state)
    await emit_event("conversation.routed", {"session_id": state["session_id"], "target_agent": target})
    return {"target_agent": target, "agent_results": [{"agent": "supervisor_agent", **result.model_dump()}]}


async def domain_node(state: OrchestratorState) -> dict[str, Any]:
    target = state.get("target_agent") or "customer_agent"
    module = importlib.import_module(f"ai_platform.agents.{target}.agent")
    schemas = importlib.import_module(f"ai_platform.agents.{target}.schemas")
    class_prefix = "".join(p.capitalize() for p in target.split("_"))
    agent_cls = getattr(module, class_prefix)
    input_cls = getattr(schemas, f"{class_prefix}Input")

    agent = agent_cls()
    result = await agent.run(
        input_cls(
            session_id=state["session_id"],
            customer_id=state["customer_id"],
            message=state["message"],
        )
    )
    results = list(state.get("agent_results", []))
    results.append(result.model_dump())
    await emit_event("conversation.completed", {"session_id": state["session_id"], "agent": target})
    return {
        "agent_results": results,
        "reply": result.message,
        "requires_escalation": result.requires_escalation,
    }
