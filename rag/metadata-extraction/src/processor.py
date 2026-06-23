"""Core processing logic for metadata-extraction."""

from typing import Any


async def process_document(data: dict[str, Any]) -> dict[str, Any]:
    """Process document through the metadata-extraction pipeline stage."""
    content = data.get("content", "")
    metadata = data.get("metadata", {})
    options = data.get("options", {})

    return {
        "service": "metadata-extraction",
        "content_length": len(content) if content else 0,
        "metadata": metadata,
        "options": options,
        "processed": True,
    }
