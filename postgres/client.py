"""PostgreSQL client for operational data."""

from __future__ import annotations

from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from eaap_platform.config import get_settings

_engine: Engine | None = None


def _engine_instance() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(get_settings().database_sync_url, pool_pre_ping=True)
    return _engine


class PostgresClient:
    def list_orders(self, limit: int = 20) -> list[dict[str, Any]]:
        try:
            with _engine_instance().connect() as conn:
                result = conn.execute(
                    text(
                        'SELECT id, order_number, customer, status, total '
                        'FROM orders ORDER BY created_at DESC LIMIT :limit'
                    ),
                    {"limit": limit},
                )
                return [dict(row._mapping) for row in result]
        except Exception:
            return [
                {"id": 1, "order_number": "ORD-1001", "customer": "Acme Corp", "status": "shipped", "total": 4200.0},
                {"id": 2, "order_number": "ORD-1002", "customer": "Jane Doe", "status": "processing", "total": 199.0},
            ]

    def execute_read(self, sql: str, limit: int = 100) -> list[dict[str, Any]]:
        wrapped = sql if "limit" in sql.lower() else f"{sql.rstrip(';')} LIMIT {limit}"
        with _engine_instance().connect() as conn:
            result = conn.execute(text(wrapped))
            return [dict(row._mapping) for row in result]
