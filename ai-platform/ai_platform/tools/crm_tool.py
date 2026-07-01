from __future__ import annotations

from ai_platform.infrastructure.crm import lookup_crm_account


async def lookup_crm(customer_id: str) -> dict:
    account = await lookup_crm_account(customer_id)
    return account.model_dump()
