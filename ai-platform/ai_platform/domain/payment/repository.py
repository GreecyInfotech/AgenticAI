from __future__ import annotations

from typing import Protocol

from ai_platform.domain.payment.entities import PaymentEntity


class PaymentRepository(Protocol):
    async def get_by_id(self, entity_id: str) -> PaymentEntity | None: ...
    async def save(self, entity: PaymentEntity) -> None: ...
