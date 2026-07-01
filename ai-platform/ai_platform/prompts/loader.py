from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

_PROMPTS_ROOT = Path(__file__).resolve().parents[3] / "prompts"


@lru_cache
def _environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(_PROMPTS_ROOT)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_template(template_name: str, **context: Any) -> str:
    """Render a Jinja2 template from the repo prompts/ directory."""
    template = _environment().get_template(template_name)
    return template.render(**context).strip()


def render_system_base() -> str:
    path = _PROMPTS_ROOT / "system" / "base.md"
    return path.read_text(encoding="utf-8").strip()
