"""PostgreSQL MCP server — read-only SQL and schema introspection."""

from __future__ import annotations

from sqlalchemy import inspect, text

from mcp.server.fastmcp import FastMCP

from eaap_platform.config import get_settings
from eaap_platform.mcp_base import error_result, text_result
from postgres.client import PostgresClient, _engine_instance

mcp = FastMCP("postgres-mcp", instructions="PostgreSQL schema exploration and read-only queries.")

BLOCKED = frozenset({"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"})


@mcp.tool()
def list_tables(schema: str = "public") -> str:
    try:
        tables = inspect(_engine_instance()).get_table_names(schema=schema)
        return text_result({"schema": schema, "tables": tables})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def execute_query(sql: str, limit: int = 100) -> str:
    try:
        token = sql.strip().split()[0].upper() if sql.strip() else ""
        if token in BLOCKED:
            return error_result(f"Blocked keyword: {token}")
        rows = PostgresClient().execute_read(sql, limit=limit)
        return text_result({"count": len(rows), "rows": rows})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def list_orders(limit: int = 20) -> str:
    try:
        return text_result({"orders": PostgresClient().list_orders(limit=limit)})
    except Exception as exc:
        return error_result(str(exc))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
