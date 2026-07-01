from __future__ import annotations

from ai_platform.infrastructure.email import send_email


async def send_email_notification(to: str, subject: str, body: str) -> dict:
    return await send_email(to, subject, body)
