"""Kafka Streams processing for vessel arrival events."""

import json
from typing import Any

from smart_port_common.logging import get_logger

logger = get_logger(__name__)

TOPICS = {
    "input": "vessel.arrivals",
    "output_berth": "berth.allocations",
    "output_agent": "agent.invocations",
    "dlq": "dlq.vessel",
}


class VesselArrivalProcessor:
    """Process vessel arrival events and trigger berth allocation."""

    async def process(self, event: dict[str, Any]) -> dict[str, Any] | None:
        required = ["vessel_id", "eta"]
        if not all(k in event for k in required):
            logger.warning("invalid_event", event=event, missing=required)
            return None

        berth_allocation = {
            "event_type": "berth.allocation.requested",
            "vessel_id": event["vessel_id"],
            "vessel_name": event.get("vessel_name"),
            "eta": event["eta"],
            "teu_count": event.get("teu_count", 0),
            "priority": self._calculate_priority(event),
        }

        logger.info("berth_allocation_triggered", vessel_id=event["vessel_id"])
        return berth_allocation

    def _calculate_priority(self, event: dict[str, Any]) -> int:
        teu = event.get("teu_count", 0)
        if teu > 10000:
            return 1
        if teu > 5000:
            return 2
        return 3


class ContainerMoveAggregator:
    """Aggregate container moves for yard utilization metrics."""

    def __init__(self) -> None:
        self._move_counts: dict[str, int] = {}

    def aggregate(self, event: dict[str, Any]) -> dict[str, Any]:
        yard = event.get("to_location", "unknown")[:5]
        self._move_counts[yard] = self._move_counts.get(yard, 0) + 1
        return {
            "event_type": "yard.status.update",
            "yard_zone": yard,
            "move_count": self._move_counts[yard],
            "timestamp": event.get("timestamp"),
        }


class DeadLetterHandler:
    """Route failed events to appropriate DLQ topics."""

    DLQ_MAP = {
        "vessel.arrivals": "dlq.vessel",
        "container.moves": "dlq.container",
        "customs.declarations": "dlq.customs",
        "agent.invocations": "dlq.agent",
    }

    @classmethod
    def get_dlq_topic(cls, source_topic: str) -> str:
        return cls.DLQ_MAP.get(source_topic, "dlq.agent")

    @classmethod
    def wrap_failure(cls, source_topic: str, event: dict, error: str) -> dict:
        return {
            "original_topic": source_topic,
            "original_event": event,
            "error": error,
            "dlq_topic": cls.get_dlq_topic(source_topic),
        }
