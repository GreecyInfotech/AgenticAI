from __future__ import annotations

from ai_platform.orchestrator.workflow import run_ordering_workflow

async def repeat_order(session_id: str, customer_id: str, order_id: str) -> dict:
    return await run_ordering_workflow(session_id, customer_id, f"repeat order {order_id}")
