from __future__ import annotations

class OktaClient:
    async def verify(self, token: str) -> bool:
        return bool(token)
