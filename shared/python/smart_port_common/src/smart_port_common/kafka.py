"""Kafka producer and consumer wrappers."""

import json
from typing import Any, Callable

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

from smart_port_common.config import get_settings
from smart_port_common.logging import get_logger

logger = get_logger(__name__)


class KafkaProducer:
    def __init__(self, client_id: str | None = None) -> None:
        settings = get_settings()
        self._producer: AIOKafkaProducer | None = None
        self._bootstrap = settings.kafka_bootstrap_servers
        self._client_id = client_id or settings.service_name

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap,
            client_id=self._client_id,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()
        logger.info("kafka_producer_started", bootstrap=self._bootstrap)

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()

    async def publish(self, topic: str, message: dict[str, Any], key: str | None = None) -> None:
        if not self._producer:
            raise RuntimeError("Producer not started")
        try:
            await self._producer.send_and_wait(
                topic,
                message,
                key=key.encode("utf-8") if key else None,
            )
            logger.info("kafka_message_published", topic=topic, key=key)
        except KafkaError as exc:
            logger.error("kafka_publish_failed", topic=topic, error=str(exc))
            raise


class KafkaConsumer:
    def __init__(self, topics: list[str], group_id: str) -> None:
        settings = get_settings()
        self._topics = topics
        self._group_id = group_id
        self._bootstrap = settings.kafka_bootstrap_servers
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        self._consumer = AIOKafkaConsumer(
            *self._topics,
            bootstrap_servers=self._bootstrap,
            group_id=self._group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        await self._consumer.start()
        logger.info("kafka_consumer_started", topics=self._topics, group=self._group_id)

    async def stop(self) -> None:
        if self._consumer:
            await self._consumer.stop()

    async def consume(self, handler: Callable[[str, dict[str, Any]], Any]) -> None:
        if not self._consumer:
            raise RuntimeError("Consumer not started")
        async for msg in self._consumer:
            await handler(msg.topic, msg.value)
