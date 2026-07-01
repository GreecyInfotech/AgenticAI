from __future__ import annotations

from ai_platform.memory.long_term_memory import LongTermMemory
from ai_platform.memory.postgres_memory import PostgresMemory
from ai_platform.memory.redis_memory import RedisMemory
from ai_platform.memory.session_memory import SessionMemory
from ai_platform.memory.summary_memory import SummaryMemory

__all__ = [
    "LongTermMemory",
    "PostgresMemory",
    "RedisMemory",
    "SessionMemory",
    "SummaryMemory",
    "get_long_term_memory",
    "get_session_memory",
    "get_summary_memory",
]


def get_session_memory(session_id: str) -> SessionMemory:
    return SessionMemory(session_id)


def get_summary_memory() -> SummaryMemory:
    return SummaryMemory()


def get_long_term_memory() -> LongTermMemory:
    return LongTermMemory()
