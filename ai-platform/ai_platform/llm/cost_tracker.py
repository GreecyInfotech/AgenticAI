from __future__ import annotations

_cost: dict[str, float] = {}


def track(provider: str, tokens: int, cost: float) -> None:
    _cost[provider] = _cost.get(provider, 0.0) + cost


def snapshot() -> dict[str, float]:
    return dict(_cost)
