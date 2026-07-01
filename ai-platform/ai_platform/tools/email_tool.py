from __future__ import annotations

async def send_email(to: str, subject: str, body: str) -> dict:
    return {"to": to, "subject": subject, "status": "sent"}
