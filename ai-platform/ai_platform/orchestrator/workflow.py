from __future__ import annotations

from ai_platform.orchestrator.executor import WorkflowExecutor


async def run_ordering_workflow(session_id: str, customer_id: str, message: str) -> dict:
    executor = WorkflowExecutor()
    state = await executor.execute(session_id, customer_id, message)
    return {
        "session_id": session_id,
        "reply": state.get("reply"),
        "target_agent": state.get("target_agent"),
        "agent_results": state.get("agent_results", []),
        "requires_escalation": state.get("requires_escalation", False),
    }
