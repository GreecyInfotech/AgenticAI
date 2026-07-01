from __future__ import annotations

from ai_platform.infrastructure.email.smtp_client import (
    EmailClient,
    SmtpEmailClient,
    check_email_health,
    get_email_client,
    get_sent_log,
    send_email,
)

__all__ = [
    "EmailClient",
    "SmtpEmailClient",
    "check_email_health",
    "get_email_client",
    "get_sent_log",
    "send_email",
]
