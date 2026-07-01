from __future__ import annotations

from typing import Literal

from ai_platform.orchestrator.state import OrchestratorState


def after_supervisor(state: OrchestratorState) -> Literal["domain", "end"]:
    if state.get("target_agent"):
        return "domain"
    return "end"
