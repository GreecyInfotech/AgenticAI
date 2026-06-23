"""Core processing logic for document-ingestion."""

from typing import Any


async def process_document(data: dict[str, Any]) -> dict[str, Any]:
    """Process document through the document-ingestion pipeline stage."""
    content = data.get("content", "")
    metadata = data.get("metadata", {})
    options = data.get("options", {})

    return {
        "service": "document-ingestion",
        "content_length": len(content) if content else 0,
        "metadata": metadata,
        "options": options,
        "processed": True,
    }
