from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header

from ai_platform.orchestrator.workflow import run_ordering_workflow
from pydantic import BaseModel, Field
from shared.exceptions import ValidationError
from shared.security import CurrentUser, is_prompt_injection, require_permission

router = APIRouter()


class ConversationRequest(BaseModel):
    session_id: str
    customer_id: str
    message: str = Field(min_length=1, max_length=4000)


class ConversationResponse(BaseModel):
    session_id: str
    reply: str | None
    target_agent: str | None
    agent_results: list[dict] = Field(default_factory=list)
    requires_escalation: bool = False


@router.post("/conversation", response_model=ConversationResponse)
async def converse(
    request: ConversationRequest,
    user: Annotated[CurrentUser, Depends(require_permission("conversation:write"))],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> ConversationResponse:
    if is_prompt_injection(request.message):
        raise ValidationError("Message rejected: potential prompt injection detected")

    if request.customer_id != user.subject and user.role != "admin":
        request = ConversationRequest(
            session_id=request.session_id,
            customer_id=user.subject,
            message=request.message,
        )

    _ = idempotency_key  # reserved for session deduplication
    result = await run_ordering_workflow(request.session_id, request.customer_id, request.message)
    return ConversationResponse(**result)
