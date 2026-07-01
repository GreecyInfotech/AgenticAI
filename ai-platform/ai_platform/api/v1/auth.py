from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from shared.security import create_access_token, get_current_user, CurrentUser

router = APIRouter()


class TokenRequest(BaseModel):
    subject: str
    role: str = "distributor"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


@router.post("/auth/token", response_model=TokenResponse)
async def issue_token(body: TokenRequest) -> TokenResponse:
    """Development token endpoint. Replace with OAuth/Okta in production."""
    from shared.config.settings import get_base_settings

    settings = get_base_settings()
    token = create_access_token(body.subject, role=body.role)
    return TokenResponse(access_token=token, expires_in_minutes=settings.jwt_expire_minutes)


@router.get("/auth/me")
async def get_me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> dict:
    return {"subject": user.subject, "role": user.role}
