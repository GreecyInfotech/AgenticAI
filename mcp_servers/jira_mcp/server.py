"""Jira MCP server."""

from __future__ import annotations

from typing import Any

from atlassian import Jira
from mcp.server.fastmcp import FastMCP

from eaap_platform.config import get_settings
from eaap_platform.mcp_base import error_result, text_result

mcp = FastMCP("jira-mcp", instructions="Jira issue search, creation, and updates.")


def _client() -> Jira:
    s = get_settings()
    if not s.jira_url or not s.jira_api_token:
        raise ValueError("JIRA_URL and JIRA_API_TOKEN required")
    return Jira(url=s.jira_url, username=s.jira_email, password=s.jira_api_token, cloud=True)


@mcp.tool()
def search_issues(jql: str, max_results: int = 25) -> str:
    try:
        result = _client().jql(jql, limit=max_results)
        issues = [
            {"key": i["key"], "summary": i["fields"]["summary"], "status": i["fields"]["status"]["name"]}
            for i in result.get("issues", [])
        ]
        return text_result({"issues": issues, "total": result.get("total", len(issues))})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> str:
    try:
        fields: dict[str, Any] = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
        result = _client().create_issue(fields=fields)
        return text_result({"created": True, "key": result.get("key")})
    except Exception as exc:
        return error_result(str(exc))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
