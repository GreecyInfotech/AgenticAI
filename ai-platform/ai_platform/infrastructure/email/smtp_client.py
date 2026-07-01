from __future__ import annotations

import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Protocol

from ai_platform.config.settings import get_settings
from shared.logging import get_logger
from shared.security.pii import mask_pii

logger = get_logger(__name__)

_sent_log: list[dict[str, str]] = []


class EmailClient(Protocol):
    async def send(self, to: str, subject: str, body: str, *, html: bool = False) -> dict[str, str]: ...


class SmtpEmailClient:
    async def send(self, to: str, subject: str, body: str, *, html: bool = False) -> dict[str, str]:
        settings = get_settings()
        if not settings.email_enabled:
            return {"status": "disabled", "to": mask_pii(to), "subject": subject}

        if not settings.smtp_host or settings.smtp_host == "localhost" and not settings.smtp_user:
            record = {"status": "logged", "to": mask_pii(to), "subject": subject}
            _sent_log.append(record)
            logger.info("email_dev_mode", to=mask_pii(to), subject=subject)
            return record

        await asyncio.to_thread(self._send_sync, to, subject, body, html)
        logger.info("email_sent", to=mask_pii(to), subject=subject)
        return {"status": "sent", "to": mask_pii(to), "subject": subject}

    def _send_sync(self, to: str, subject: str, body: str, html: bool) -> None:
        settings = get_settings()
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.smtp_from
        message["To"] = to
        subtype = "html" if html else "plain"
        message.attach(MIMEText(body, subtype, "utf-8"))

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
            if settings.smtp_use_tls:
                server.starttls()
            if settings.smtp_user:
                server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.smtp_from, [to], message.as_string())


_client: EmailClient | None = None


def get_email_client() -> EmailClient:
    global _client
    if _client is None:
        _client = SmtpEmailClient()
    return _client


async def send_email(to: str, subject: str, body: str, *, html: bool = False) -> dict[str, str]:
    return await get_email_client().send(to, subject, body, html=html)


async def check_email_health() -> dict[str, str]:
    settings = get_settings()
    if not settings.email_enabled:
        return {"status": "DISABLED"}
    if not settings.smtp_user:
        return {"status": "UP", "mode": "dev-log"}
    try:
        await asyncio.to_thread(_smtp_ping)
        return {"status": "UP", "mode": "smtp"}
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc)}


def _smtp_ping() -> None:
    settings = get_settings()
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=5) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_user:
            server.login(settings.smtp_user, settings.smtp_password)


def get_sent_log() -> list[dict[str, str]]:
    return list(_sent_log)
