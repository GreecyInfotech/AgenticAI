"""Filesystem MCP server — safe file read/list within configured root."""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from eaap_platform.config import get_settings
from eaap_platform.mcp_base import error_result, text_result

mcp = FastMCP("filesystem-mcp", instructions="Read and list files within the configured filesystem root.")


def _resolve(path: str) -> Path:
    settings = get_settings()
    root = Path(settings.filesystem_mcp_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = (root / path).resolve()
    if not str(target).startswith(str(root)):
        raise ValueError("Path outside allowed root")
    return target


@mcp.tool()
def list_directory(relative_path: str = ".") -> str:
    try:
        target = _resolve(relative_path)
        if not target.is_dir():
            return error_result("Not a directory")
        entries = [
            {"name": p.name, "type": "dir" if p.is_dir() else "file", "size": p.stat().st_size if p.is_file() else None}
            for p in sorted(target.iterdir())
        ]
        return text_result({"path": str(target), "entries": entries})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def read_file(relative_path: str, max_chars: int = 20000) -> str:
    try:
        target = _resolve(relative_path)
        if not target.is_file():
            return error_result("Not a file")
        content = target.read_text(encoding="utf-8", errors="replace")
        return text_result({"path": str(target), "content": content[:max_chars]})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def write_file(relative_path: str, content: str) -> str:
    try:
        target = _resolve(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return text_result({"written": True, "path": str(target), "bytes": len(content.encode())})
    except Exception as exc:
        return error_result(str(exc))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
