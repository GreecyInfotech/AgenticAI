from __future__ import annotations

async def send_sms(phone: str, message: str) -> dict:
    return {"phone": phone, "status": "sent"}
