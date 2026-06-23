"""GitHub MCP server."""

from __future__ import annotations

import base64

from github import Github
from mcp.server.fastmcp import FastMCP

from eaap_platform.config import get_settings
from eaap_platform.mcp_base import error_result, text_result

mcp = FastMCP("github-mcp", instructions="GitHub repos, PRs, issues, and code search.")


def _client() -> Github:
    token = get_settings().github_token
    if not token:
        raise ValueError("GITHUB_TOKEN required")
    return Github(token)


@mcp.tool()
def list_repos(org: str = "", per_page: int = 20) -> str:
    try:
        gh = _client()
        target = org or get_settings().github_org
        repos = gh.get_organization(target).get_repos() if target else gh.get_user().get_repos()
        data = [{"full_name": r.full_name, "language": r.language} for i, r in enumerate(repos) if i < per_page]
        return text_result({"repos": data})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def search_code(query: str, repo: str = "", per_page: int = 15) -> str:
    try:
        q = f"{query} repo:{repo}" if repo else query
        results = _client().search_code(q)
        items = [{"path": r.path, "repo": r.repository.full_name} for i, r in enumerate(results) if i < per_page]
        return text_result({"results": items})
    except Exception as exc:
        return error_result(str(exc))


@mcp.tool()
def get_file_contents(repo: str, path: str, ref: str = "main") -> str:
    try:
        content = _client().get_repo(repo).get_contents(path, ref=ref)
        if isinstance(content, list):
            return text_result({"type": "directory", "entries": [c.path for c in content]})
        decoded = base64.b64decode(content.content).decode("utf-8", errors="replace")
        return text_result({"path": path, "content": decoded})
    except Exception as exc:
        return error_result(str(exc))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
