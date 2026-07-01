from __future__ import annotations

from shared.constants.topics import ALL_TOPICS
from shared.messaging import (
    check_kafka_health,
    close_kafka_producer,
    get_buffered_count,
    get_buffered_events,
    init_kafka_producer,
    publish,
    start_kafka_consumer,
)

__all__ = [
    "ALL_TOPICS",
    "check_kafka_health",
    "close_kafka_producer",
    "ensure_topics",
    "get_buffered_count",
    "get_buffered_events",
    "init_kafka_producer",
    "publish",
    "start_kafka_consumer",
]


async def ensure_topics() -> None:
    """Create platform Kafka topics if auto-create is enabled."""
    from ai_platform.config.settings import get_settings

    settings = get_settings()
    if not settings.kafka_enabled or not settings.kafka_auto_create_topics:
        return

    try:
        from aiokafka import AIOKafkaAdminClient
        from aiokafka.admin import NewTopic

        admin = AIOKafkaAdminClient(bootstrap_servers=settings.kafka_bootstrap_servers)
        await admin.start()
        try:
            existing = await admin.list_topics()
            new_topics = [
                NewTopic(name=topic, num_partitions=3, replication_factor=1)
                for topic in sorted(ALL_TOPICS)
                if topic not in existing
            ]
            if new_topics:
                await admin.create_topics(new_topics)
        finally:
            await admin.close()
    except Exception as exc:
        from shared.logging import get_logger

        get_logger(__name__).warning("kafka_topic_creation_failed", error=str(exc))
