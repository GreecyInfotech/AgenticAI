from __future__ import annotations

from ai_platform.domain.payment.entities import PaymentEntity
from ai_platform.domain.payment.repository import PaymentRepository


class PaymentService:
    def __init__(self, repository: PaymentRepository) -> None:
        self._repository = repository

    async def get(self, entity_id: str) -> PaymentEntity | None:
        return await self._repository.get_by_id(entity_id)
