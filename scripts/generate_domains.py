"""Generate domain layer files."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "ai-platform" / "ai_platform" / "domain"
DOMAINS = ["customer", "product", "order", "inventory", "pricing", "payment", "shipment", "promotion"]

for domain in DOMAINS:
    d = ROOT / domain
    d.mkdir(parents=True, exist_ok=True)
    (d / "__init__.py").write_text(f'"""{domain} domain."""\n', encoding="utf-8")
    (d / "entities.py").write_text(
        f'''from __future__ import annotations

from pydantic import BaseModel


class {domain.capitalize()}Entity(BaseModel):
    id: str
    name: str
''',
        encoding="utf-8",
    )
    (d / "value_objects.py").write_text(
        f'''from __future__ import annotations

from pydantic import BaseModel


class {domain.capitalize()}Id(BaseModel):
    value: str
''',
        encoding="utf-8",
    )
    (d / "repository.py").write_text(
        f'''from __future__ import annotations

from typing import Protocol

from ai_platform.domain.{domain}.entities import {domain.capitalize()}Entity


class {domain.capitalize()}Repository(Protocol):
    async def get_by_id(self, entity_id: str) -> {domain.capitalize()}Entity | None: ...
    async def save(self, entity: {domain.capitalize()}Entity) -> None: ...
''',
        encoding="utf-8",
    )
    (d / "service.py").write_text(
        f'''from __future__ import annotations

from ai_platform.domain.{domain}.entities import {domain.capitalize()}Entity
from ai_platform.domain.{domain}.repository import {domain.capitalize()}Repository


class {domain.capitalize()}Service:
    def __init__(self, repository: {domain.capitalize()}Repository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> {domain.capitalize()}Entity | None:
        return await self._repository.get_by_id(entity_id)
''',
        encoding="utf-8",
    )
    (d / "events.py").write_text(
        f'''from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def {domain}_event(event_type: str, payload: dict) -> dict:
    return {{
        "event_id": str(uuid4()),
        "domain": "{domain}",
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }}
''',
        encoding="utf-8",
    )

print(f"Generated {len(DOMAINS)} domains")
