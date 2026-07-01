from __future__ import annotations

from ai_platform.orchestrator.graph import orchestrator_graph
from ai_platform.orchestrator.state import OrchestratorState


class WorkflowExecutor:
    async def execute(self, session_id: str, customer_id: str, message: str) -> OrchestratorState:
        initial: OrchestratorState = {
            "session_id": session_id,
            "customer_id": customer_id,
            "message": message,
            "target_agent": None,
            "agent_results": [],
            "reply": None,
            "requires_escalation": False,
        }
        result = await orchestrator_graph.ainvoke(initial)
        return result  # type: ignore[return-value]


class WorkflowExecutorSync:
    def execute(self, session_id: str, customer_id: str, message: str) -> OrchestratorState:
        import asyncio

        return asyncio.get_event_loop().run_until_complete(
            WorkflowExecutor().execute(session_id, customer_id, message)
        )
