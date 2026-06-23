"""Kafka event streaming client."""

from __future__ import annotations

import json
from typing import Any

from eaap_platform.config import get_settings
from eaap_platform.logging import get_logger

logger = get_logger(__name__)


class KafkaClient:
    async def publish(self, topic: str, message: dict[str, Any]) -> None:
        try:
            from aiokafka import AIOKafkaProducer

            settings = get_settings()
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await producer.start()
            try:
                await producer.send_and_wait(topic, message)
                logger.info("kafka_published", topic=topic)
            finally:
                await producer.stop()
        except Exception as exc:
            logger.warning("kafka_publish_fallback", topic=topic, error=str(exc))
