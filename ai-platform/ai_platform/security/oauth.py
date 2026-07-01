from __future__ import annotations

class OAuthClient:
    async def authenticate(self, token: str) -> dict | None:
        return {"sub": "user-001"} if token else None
