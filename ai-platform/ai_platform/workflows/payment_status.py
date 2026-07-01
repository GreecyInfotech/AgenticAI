from __future__ import annotations

from ai_platform.orchestrator.workflow import run_ordering_workflow

async def payment_status(session_id: str, customer_id: str, order_id: str) -> dict:
    return await run_ordering_workflow(session_id, customer_id, f"payment status {order_id}")
