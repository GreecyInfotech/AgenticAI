from __future__ import annotations

from ai_platform.orchestrator.state import OrchestratorState

AGENT_KEYWORDS: dict[str, list[str]] = {
    "order_agent": ["order", "place", "buy", "purchase"],
    "inventory_agent": ["stock", "inventory", "available", "availability"],
    "pricing_agent": ["price", "quote", "cost", "rate"],
    "promotion_agent": ["promotion", "discount", "offer", "deal"],
    "credit_agent": ["credit", "limit", "terms", "payment terms"],
    "shipment_agent": ["ship", "track", "delivery", "logistics"],
    "payment_agent": ["pay", "payment", "invoice", "balance"],
    "recommendation_agent": ["recommend", "suggest", "alternative"],
    "customer_agent": ["account", "profile", "customer"],
    "knowledge_agent": ["help", "faq", "how to", "policy"],
}


def route(state: OrchestratorState) -> str:
    message = state["message"].lower()
    for agent, keywords in AGENT_KEYWORDS.items():
        if any(kw in message for kw in keywords):
            return agent
    return "customer_agent"
