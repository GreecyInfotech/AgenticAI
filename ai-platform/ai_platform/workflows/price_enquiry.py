from __future__ import annotations

from ai_platform.orchestrator.workflow import run_ordering_workflow

async def price_enquiry(session_id: str, customer_id: str, sku: str) -> dict:
    return await run_ordering_workflow(session_id, customer_id, f"price for {sku}")
