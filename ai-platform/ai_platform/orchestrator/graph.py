from __future__ import annotations

from langgraph.graph import END, StateGraph

from ai_platform.orchestrator.edges import after_supervisor
from ai_platform.orchestrator.nodes import domain_node, supervisor_node
from ai_platform.orchestrator.state import OrchestratorState


def build_graph():
    graph = StateGraph(OrchestratorState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("domain", domain_node)
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges("supervisor", after_supervisor, {"domain": "domain", "end": END})
    graph.add_edge("domain", END)
    return graph.compile()


orchestrator_graph = build_graph()
