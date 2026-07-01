from __future__ import annotations

from ai_platform.application.dto.conversation_dto import ConversationRequestDTO, ConversationResponseDTO
from ai_platform.orchestrator.workflow import run_ordering_workflow
from shared.exceptions import ValidationError
from shared.security import is_prompt_injection


class ConversationHandler:
    async def handle(self, request: ConversationRequestDTO) -> ConversationResponseDTO:
        if is_prompt_injection(request.message):
            raise ValidationError("Message rejected: potential prompt injection detected")

        result = await run_ordering_workflow(
            request.session_id,
            request.customer_id,
            request.message,
        )
        return ConversationResponseDTO(**result)
