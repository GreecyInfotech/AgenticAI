"""Core processing logic for vector-search."""

from typing import Any


async def process_document(data: dict[str, Any]) -> dict[str, Any]:
    """Process document through the vector-search pipeline stage."""
    content = data.get("content", "")
    metadata = data.get("metadata", {})
    options = data.get("options", {})

    return {
        "service": "vector-search",
        "content_length": len(content) if content else 0,
        "metadata": metadata,
        "options": options,
        "processed": True,
    }
