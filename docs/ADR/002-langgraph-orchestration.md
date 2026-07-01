# ADR-002: LangGraph Multi-Agent Orchestration

**Status:** Accepted  
**Date:** 2026-07-01  
**Deciders:** Platform Team

## Context

Distributor ordering involves multiple domains: inventory, pricing, credit, orders, shipments, payments. A single monolithic LLM prompt cannot reliably handle all domains. We need a routing mechanism that directs user intent to specialist agents.

## Decision

Use **LangGraph** for multi-agent orchestration with:

- **Supervisor pattern** — a supervisor agent classifies intent, then routes to a specialist
- **14 specialist agents** — one per business domain
- **2-node graph** — `supervisor_node → domain_node → END`
- **Keyword routing** — `router.py` matches message keywords to agents (with LLM classification as supplement)
- **Immutable state** — each node returns new state dict, never mutates in place
- **Event emission** — `emit_event()` after significant state transitions

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|-------------|
| Single LLM with tools | Poor routing accuracy across 14 domains |
| Manual if/else routing | Not scalable, no LLM reasoning |
| AutoGen / CrewAI | Less control over state and typed transitions |
| Direct agent calls | Violates orchestrator-only routing rule |

## Consequences

### Positive

- Typed state transitions via Pydantic models
- Each agent is independently testable
- Graph is visualizable and debuggable
- Easy to add new agents without changing existing ones

### Negative

- Only one specialist agent per conversation turn (no multi-agent chains yet)
- Keyword routing is simplistic; LLM routing not fully wired
- 3 agents unreachable via current keyword map (analytics, document, notification)

## Implementation

```
ai-platform/ai_platform/orchestrator/
├── graph.py      # LangGraph StateGraph definition
├── nodes.py      # supervisor_node, domain_node
├── router.py     # AGENT_KEYWORDS mapping
├── executor.py   # WorkflowExecutor
├── workflow.py   # run_ordering_workflow() public API
├── events.py     # Kafka event emission
└── state.py      # OrchestratorState TypedDict
```

## References

- `.cursor/rules/langgraph.mdc`
- `.cursor/rules/ai-agent.mdc`
- `docs/sequence-diagrams/conversation-flow.md`
