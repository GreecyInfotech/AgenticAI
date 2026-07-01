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
_consumer: Any = None
_consumer_task: asyncio.Task[None] | None = None
_fallback_events: list[dict[str, Any]] = []
_buffered_count: int = 0


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
            acks="all",
            enable_idempotence=True,
        )
        await asyncio.wait_for(_producer.start(), timeout=5.0)
        logger.info("kafka_producer_started", servers=settings.kafka_bootstrap_servers)
    except Exception as exc:
        logger.warning("kafka_producer_unavailable", error=str(exc))
        _producer = None


async def close_kafka_producer() -> None:
    global _producer, _consumer, _consumer_task
    if _consumer_task is not None:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            pass
        _consumer_task = None
    if _consumer is not None:
        await _consumer.stop()
        _consumer = None
    if _producer is not None:
        await _producer.stop()
        _producer = None


async def publish(topic: str, event: DomainEvent | dict[str, Any]) -> None:
    global _buffered_count
    if topic not in ALL_TOPICS:
        logger.warning("unknown_topic", topic=topic)

    payload = event.to_dict() if isinstance(event, DomainEvent) else event

    if _producer is None:
        _fallback_events.append({"topic": topic, "event": payload})
        _buffered_count += 1
        logger.info("kafka_event_buffered", topic=topic, event_id=payload.get("event_id"))
        return

    await _producer.send_and_wait(topic, payload)
    logger.info("kafka_event_published", topic=topic, event_id=payload.get("event_id"))


def get_buffered_events() -> list[dict[str, Any]]:
    return list(_fallback_events)


def get_buffered_count() -> int:
    return _buffered_count


async def check_kafka_health() -> dict[str, Any]:
    settings = get_base_settings()
    if not settings.kafka_enabled:
        return {"status": "DISABLED"}
    if _producer is None:
        return {
            "status": "DOWN",
            "detail": "producer not initialized",
            "buffered_events": _buffered_count,
        }
    try:
        from aiokafka import AIOKafkaAdminClient

        admin = AIOKafkaAdminClient(bootstrap_servers=settings.kafka_bootstrap_servers)
        await admin.start()
        try:
            topics = await admin.list_topics()
            return {
                "status": "UP",
                "topics": len(topics),
                "buffered_events": _buffered_count,
            }
        finally:
            await admin.close()
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc), "buffered_events": _buffered_count}


async def start_kafka_consumer(handler: Any | None = None) -> None:
    """Start background consumer for platform events."""
    global _consumer, _consumer_task
    settings = get_base_settings()
    if not settings.kafka_enabled:
        return
    try:
        from aiokafka import AIOKafkaConsumer

        _consumer = AIOKafkaConsumer(
            *sorted(ALL_TOPICS),
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=getattr(settings, "kafka_consumer_group", "ai-platform"),
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        await _consumer.start()
        logger.info("kafka_consumer_started", topics=len(ALL_TOPICS))

        async def _consume() -> None:
            assert _consumer is not None
            async for message in _consumer:
                payload = message.value
                logger.info(
                    "kafka_event_received",
                    topic=message.topic,
                    event_id=payload.get("event_id"),
                )
                if handler is not None:
                    await handler(message.topic, payload)

        _consumer_task = asyncio.create_task(_consume())
    except Exception as exc:
        logger.warning("kafka_consumer_unavailable", error=str(exc))
        _consumer = None
