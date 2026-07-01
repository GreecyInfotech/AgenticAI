from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header

from ai_platform.application.dto.conversation_dto import ConversationRequestDTO, ConversationResponseDTO
from ai_platform.application.use_cases.conversation import ConversationUseCase
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.post("/conversation", response_model=ConversationResponseDTO)
async def converse(
    request: ConversationRequestDTO,
    user: Annotated[CurrentUser, Depends(require_permission("conversation:write"))],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> ConversationResponseDTO:
    if request.customer_id != user.subject and user.role != "admin":
        request = ConversationRequestDTO(
            session_id=request.session_id,
            customer_id=user.subject,
            message=request.message,
        )

    _ = idempotency_key  # reserved for session deduplication
    return await ConversationUseCase().execute(request)
