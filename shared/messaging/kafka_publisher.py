from __future__ import annotations

import asyncio
import json
from typing import Any

from shared.config.settings import get_base_settings
from shared.constants.topics import ALL_TOPICS
from shared.logging import get_logger
from shared.messaging.events.schemas import DomainEvent

logger = get_logger(__name__)

_producer: Any = None
_fallback_events: list[dict[str, Any]] = []


async def init_kafka_producer() -> None:
    global _producer
    settings = get_base_settings()
    if not settings.kafka_enabled:
        logger.warning("kafka_disabled")
        return
    try:
        from aiokafka import AIOKafkaProducer

        _producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            request_timeout_ms=5000,
        )
        await asyncio.wait_for(_producer.start(), timeout=5.0)
        logger.info("kafka_producer_started", servers=settings.kafka_bootstrap_servers)
    except Exception as exc:
        logger.warning("kafka_producer_unavailable", error=str(exc))
        _producer = None


async def close_kafka_producer() -> None:
    global _producer
    if _producer is not None:
        await _producer.stop()
        _producer = None


async def publish(topic: str, event: DomainEvent | dict[str, Any]) -> None:
    if topic not in ALL_TOPICS:
        logger.warning("unknown_topic", topic=topic)

    payload = event.to_dict() if isinstance(event, DomainEvent) else event

    if _producer is None:
        _fallback_events.append({"topic": topic, "event": payload})
        logger.info("kafka_event_buffered", topic=topic, event_id=payload.get("event_id"))
        return

    await _producer.send_and_wait(topic, payload)
    logger.info("kafka_event_published", topic=topic, event_id=payload.get("event_id"))


def get_buffered_events() -> list[dict[str, Any]]:
    return list(_fallback_events)
