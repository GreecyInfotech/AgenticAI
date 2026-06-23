"""Core processing logic for chunking."""

from typing import Any


async def process_document(data: dict[str, Any]) -> dict[str, Any]:
    """Process document through the chunking pipeline stage."""
    content = data.get("content", "")
    metadata = data.get("metadata", {})
    options = data.get("options", {})

    return {
        "service": "chunking",
        "content_length": len(content) if content else 0,
        "metadata": metadata,
        "options": options,
        "processed": True,
    }
