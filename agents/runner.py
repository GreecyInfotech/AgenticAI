"""Agent definitions and execution engine."""

from __future__ import annotations

import json
from typing import Any

from eaap_platform.config import get_settings
from eaap_platform.http_client import ServiceClient
from kafka.client import KafkaClient

AGENT_REGISTRY: dict[str, dict[str, Any]] = {
    "support": {
        "name": "support-agent",
        "description": "Customer support triage, knowledge lookup, and ticket routing.",
        "system": "You are a support agent for B2B and B2C customers.",
        "tools": ["search_knowledge", "search_jira", "publish_event"],
    },
    "backlog": {
        "name": "backlog-agent",
        "description": "Sprint planning, backlog prioritization, and Jira management.",
        "system": "You are a product backlog and sprint planning agent.",
        "tools": ["search_jira", "create_jira_issue"],
    },
    "architecture": {
        "name": "architecture-agent",
        "description": "System design review, ADR lookup, and GitHub code analysis.",
        "system": "You are an enterprise architecture agent.",
        "tools": ["search_github", "read_file", "search_knowledge"],
    },
    "sales": {
        "name": "sales-agent",
        "description": "Lead qualification, pipeline insights, and proposal support.",
        "system": "You are a B2B sales enablement agent.",
        "tools": ["search_knowledge", "publish_event"],
    },
    "order": {
        "name": "order-agent",
        "description": "Order status, fulfillment tracking, and order event publishing.",
        "system": "You are an order management agent.",
        "tools": ["list_orders", "publish_order_event"],
    },
}


async def _tool_search_knowledge(query: str) -> str:
    settings = get_settings()
    client = ServiceClient(settings.rag_service_url)
    return json.dumps(await client.post("/search", {"query": query, "top_k": 5}))


async def _tool_search_jira(query: str) -> str:
    try:
        from atlassian import Jira

        settings = get_settings()
        if not settings.jira_url or not settings.jira_api_token:
            return json.dumps({"error": "Jira not configured"})
        jira = Jira(
            url=settings.jira_url,
            username=settings.jira_email,
            password=settings.jira_api_token,
            cloud=True,
        )
        result = jira.jql(f'text ~ "{query}" ORDER BY created DESC', limit=10)
        return json.dumps(result)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


async def _tool_create_jira_issue(query: str) -> str:
    try:
        from atlassian import Jira

        settings = get_settings()
        jira = Jira(
            url=settings.jira_url,
            username=settings.jira_email,
            password=settings.jira_api_token,
            cloud=True,
        )
        result = jira.create_issue(
            fields={
                "project": {"key": "EAAP"},
                "summary": query[:100],
                "description": query,
                "issuetype": {"name": "Task"},
            }
        )
        return json.dumps({"created": True, "key": result.get("key")})
    except Exception as exc:
        return json.dumps({"error": str(exc)})


async def _tool_search_github(query: str) -> str:
    try:
        from github import Github

        settings = get_settings()
        if not settings.github_token:
            return json.dumps({"error": "GitHub not configured"})
        gh = Github(settings.github_token)
        results = gh.search_code(query)
        items = [{"path": r.path, "repo": r.repository.full_name} for i, r in enumerate(results) if i < 10]
        return json.dumps({"results": items})
    except Exception as exc:
        return json.dumps({"error": str(exc)})


async def _tool_read_file(query: str) -> str:
    from pathlib import Path

    settings = get_settings()
    root = Path(settings.filesystem_mcp_root).resolve()
    target = (root / query).resolve()
    if not str(target).startswith(str(root)):
        return json.dumps({"error": "Path outside allowed root"})
    if not target.exists():
        return json.dumps({"error": "File not found"})
    return json.dumps({"path": str(target), "content": target.read_text(encoding="utf-8")[:10000]})


async def _tool_list_orders(_query: str) -> str:
    from postgres.client import PostgresClient

    return json.dumps({"orders": PostgresClient().list_orders()})


async def _tool_publish_event(query: str) -> str:
    settings = get_settings()
    await KafkaClient().publish(
        settings.kafka_agent_events_topic,
        {"event": "agent_action", "payload": query},
    )
    return json.dumps({"published": True, "topic": settings.kafka_agent_events_topic})


async def _tool_publish_order_event(query: str) -> str:
    settings = get_settings()
    await KafkaClient().publish(
        settings.kafka_order_events_topic,
        {"event": "order_update", "payload": query},
    )
    return json.dumps({"published": True, "topic": settings.kafka_order_events_topic})


TOOL_HANDLERS = {
    "search_knowledge": _tool_search_knowledge,
    "search_jira": _tool_search_jira,
    "create_jira_issue": _tool_create_jira_issue,
    "search_github": _tool_search_github,
    "read_file": _tool_read_file,
    "list_orders": _tool_list_orders,
    "publish_event": _tool_publish_event,
    "publish_order_event": _tool_publish_order_event,
}


async def run_agent(agent_id: str, query: str, context: dict[str, Any]) -> dict[str, Any]:
    spec = AGENT_REGISTRY[agent_id]
    actions: list[str] = []
    tool_results: list[dict[str, Any]] = []

    for tool_name in spec["tools"][:2]:
        handler = TOOL_HANDLERS.get(tool_name)
        if handler:
            result = await handler(query)
            actions.append(f"{tool_name}({json.dumps({'query': query[:80]})})")
            tool_results.append({"tool": tool_name, "result": result})

    portal = context.get("portal", "b2b")
    answer = (
        f"[{spec['name']}] Processed your request for {portal} portal. "
        f"Executed {len(actions)} tool(s). Summary: {query[:200]}"
    )
    return {
        "agent": agent_id,
        "answer": answer,
        "actions_taken": actions,
        "metadata": {"tool_results": tool_results, "portal": portal},
    }
