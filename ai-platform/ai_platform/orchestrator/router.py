from __future__ import annotations

import json
import re
from typing import Any

from ai_platform.orchestrator.state import OrchestratorState
from ai_platform.telemetry.metrics import record_orchestrator_route
from shared.logging import get_logger

logger = get_logger(__name__)

VALID_AGENTS = {
    "order_agent",
    "inventory_agent",
    "pricing_agent",
    "promotion_agent",
    "credit_agent",
    "shipment_agent",
    "payment_agent",
    "recommendation_agent",
    "customer_agent",
    "knowledge_agent",
}

AGENT_KEYWORDS: dict[str, list[str]] = {
    "order_agent": ["order", "place", "buy", "purchase", "cancel"],
    "inventory_agent": ["stock", "inventory", "available", "availability"],
    "pricing_agent": ["price", "quote", "cost", "rate"],
    "promotion_agent": ["promotion", "discount", "offer", "deal"],
    "credit_agent": ["credit", "limit", "terms", "payment terms"],
    "shipment_agent": ["ship", "track", "delivery", "logistics"],
    "payment_agent": ["pay", "payment", "invoice", "balance"],
    "recommendation_agent": ["recommend", "suggest", "alternative"],
    "customer_agent": ["account", "profile", "customer"],
    "knowledge_agent": ["help", "faq", "how to", "policy", "return"],
}


def route_by_keywords(state: OrchestratorState) -> str:
    message = state["message"].lower()
    for agent, keywords in AGENT_KEYWORDS.items():
        if any(kw in message for kw in keywords):
            return agent
    return "customer_agent"


def parse_supervisor_routing(supervisor_message: str) -> dict[str, Any] | None:
    try:
        match = re.search(r"\{.*\}", supervisor_message, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group())
        target = data.get("target_agent")
        if target in VALID_AGENTS:
            return data
    except (json.JSONDecodeError, TypeError):
        return None
    return None


def route(state: OrchestratorState, supervisor_message: str | None = None) -> str:
    if supervisor_message:
        parsed = parse_supervisor_routing(supervisor_message)
        if parsed:
            target = str(parsed["target_agent"])
            record_orchestrator_route(target)
            logger.info("supervisor_route_selected", target_agent=target, reasoning=parsed.get("reasoning"))
            return target

    target = route_by_keywords(state)
    record_orchestrator_route(target)
    logger.info("keyword_route_selected", target_agent=target)
    return target
