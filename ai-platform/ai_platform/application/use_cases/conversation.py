from __future__ import annotations

from ai_platform.application.dto.conversation_dto import ConversationRequestDTO, ConversationResponseDTO
from ai_platform.application.handlers.conversation_handler import ConversationHandler


class ConversationUseCase:
    def __init__(self) -> None:
        self._handler = ConversationHandler()

    async def execute(self, request: ConversationRequestDTO) -> ConversationResponseDTO:
        return await self._handler.handle(request)
