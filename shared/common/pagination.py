from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    cursor: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None = None
    total: int | None = None


def encode_cursor(offset: int) -> str:
    return str(offset)


def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    try:
        return max(0, int(cursor))
    except ValueError:
        return 0


def paginate(items: list[Any], *, limit: int, cursor: str | None = None) -> PaginatedResponse[Any]:
    offset = decode_cursor(cursor)
    page = items[offset : offset + limit]
    next_offset = offset + limit
    next_cursor = encode_cursor(next_offset) if next_offset < len(items) else None
    return PaginatedResponse(items=page, next_cursor=next_cursor, total=len(items))
