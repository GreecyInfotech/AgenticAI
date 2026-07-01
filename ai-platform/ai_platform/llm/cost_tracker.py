from __future__ import annotations

# Per-1K token pricing estimates (USD) for cost tracking
_MODEL_PRICING: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "text-embedding-3-small": {"input": 0.00002, "output": 0.0},
}

_usage: dict[str, dict[str, float]] = {}


def _count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    try:
        import tiktoken

        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return max(1, len(text) // 4)


def estimate_cost(prompt: str, response: str, provider: str, model: str = "gpt-4o-mini") -> dict[str, float]:
    input_tokens = _count_tokens(prompt, model)
    output_tokens = _count_tokens(response, model)
    pricing = _MODEL_PRICING.get(model, _MODEL_PRICING["gpt-4o-mini"])
    cost = (input_tokens / 1000 * pricing["input"]) + (output_tokens / 1000 * pricing["output"])
    return {
        "input_tokens": float(input_tokens),
        "output_tokens": float(output_tokens),
        "total_tokens": float(input_tokens + output_tokens),
        "estimated_cost_usd": round(cost, 6),
    }


def track_usage(provider: str, tokens: float, cost_usd: float) -> None:
    bucket = _usage.setdefault(provider, {"tokens": 0.0, "cost_usd": 0.0})
    bucket["tokens"] += tokens
    bucket["cost_usd"] += cost_usd


def snapshot() -> dict[str, dict[str, float]]:
    return {provider: dict(stats) for provider, stats in _usage.items()}
