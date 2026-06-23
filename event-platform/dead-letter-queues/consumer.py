"""Dead letter queue consumer for failed event reprocessing."""

import asyncio
from typing import Any

from smart_port_common.kafka import KafkaConsumer, KafkaProducer
from smart_port_common.logging import get_logger, setup_logging

logger = get_logger(__name__)

DLQ_TOPICS = ["dlq.vessel", "dlq.container", "dlq.customs", "dlq.agent"]
MAX_RETRIES = 3


async def reprocess_message(topic: str, message: dict[str, Any], producer: KafkaProducer) -> None:
    original_topic = message.get("original_topic", "")
    original_event = message.get("original_event", {})
    retry_count = message.get("retry_count", 0)

    if retry_count >= MAX_RETRIES:
        logger.error("dlq_max_retries_exceeded", topic=topic, event=original_event)
        return

    logger.info("dlq_reprocessing", original_topic=original_topic, retry=retry_count + 1)
    await producer.publish(original_topic, {**original_event, "retry_count": retry_count + 1})


async def main() -> None:
    setup_logging("dlq-consumer")
    producer = KafkaProducer(client_id="dlq-consumer")
    consumer = KafkaConsumer(DLQ_TOPICS, group_id="dlq-reprocessor")

    await producer.start()
    await consumer.start()

    try:
        await consumer.consume(lambda topic, msg: reprocess_message(topic, msg, producer))
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
