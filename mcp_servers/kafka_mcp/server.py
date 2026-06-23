"""Kafka MCP server — publish and describe topics."""

from __future__ import annotations

import asyncio
import json

from mcp.server.fastmcp import FastMCP

from eaap_platform.config import get_settings
from eaap_platform.mcp_base import error_result, text_result
from kafka.client import KafkaClient

mcp = FastMCP("kafka-mcp", instructions="Kafka topic publishing and platform event streaming.")


@mcp.tool()
def publish_message(topic: str, message_json: str) -> str:
    """Publish a JSON message to a Kafka topic."""
    try:
        payload = json.loads(message_json)
        if not isinstance(payload, dict):
            return error_result("message_json must be a JSON object")
        asyncio.run(KafkaClient().publish(topic, payload))
        return text_result({"published": True, "topic": topic})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def list_default_topics() -> str:
    try:
        s = get_settings()
        return text_result(
            {
                "bootstrap_servers": s.kafka_bootstrap_servers,
                "topics": [s.kafka_agent_events_topic, s.kafka_order_events_topic],
            }
        )
    except Exception as exc:
        return error_result(str(exc))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
