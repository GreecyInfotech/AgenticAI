# Conversation Flow Sequence Diagram

How the LangGraph orchestrator processes AI conversation requests.

## Full Conversation Flow

```mermaid
sequenceDiagram
    actor User
    participant API as /api/v1/conversation
    participant GUARD as Prompt Injection Guard
    participant AUTH as JWT + RBAC
    participant WF as WorkflowExecutor
    participant GRAPH as LangGraph
    participant SUP as supervisor_node
    participant ROUTE as router.py
    participant DOM as domain_node
    participant AGENT as Specialist Agent
    participant LLM as LLM Provider
    participant KF as Kafka

    User->>API: POST {session_id, customer_id, message}
    API->>AUTH: require_permission(conversation:write)
    API->>GUARD: is_prompt_injection(message)
    alt Injection detected
        GUARD-->>API: ValidationError 422
    end
    API->>WF: execute(session_id, customer_id, message)
    WF->>GRAPH: ainvoke(initial_state)

    Note over GRAPH: Node 1: supervisor_node
    GRAPH->>SUP: run supervisor
    SUP->>AGENT: SupervisorAgent.run()
    AGENT->>LLM: ainvoke(prompt)
    LLM-->>AGENT: classification response
    SUP->>ROUTE: route(state) keyword matching
    ROUTE-->>SUP: target_agent (e.g. inventory_agent)
    SUP->>KF: emit(conversation.routed)

    Note over GRAPH: Node 2: domain_node
    GRAPH->>DOM: run domain agent
    DOM->>AGENT: dynamic import + run
    AGENT->>LLM: ainvoke(domain prompt)
    LLM-->>AGENT: domain response
    DOM->>KF: emit(conversation.completed)
    DOM-->>GRAPH: {reply, agent_results, requires_escalation}

    GRAPH-->>WF: final state
    WF-->>API: ConversationResponse
    API-->>User: JSON response
```

## Agent Routing Keywords

| Agent | Trigger Keywords |
|-------|-----------------|
| order_agent | order, place, buy, purchase |
| inventory_agent | stock, inventory, available, availability |
| pricing_agent | price, quote, cost, rate |
| promotion_agent | promotion, discount, offer, deal |
| credit_agent | credit, limit, terms, payment terms |
| shipment_agent | ship, track, delivery, logistics |
| payment_agent | pay, payment, invoice, balance |
| recommendation_agent | recommend, suggest, alternative |
| customer_agent | account, profile, customer |
| knowledge_agent | help, faq, how to, policy |
| *(default)* | customer_agent |

## Graph Structure

```
START → supervisor_node → domain_node → END
```

Defined in `ai-platform/ai_platform/orchestrator/graph.py`.

## State Schema

```python
class OrchestratorState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    target_agent: str | None
    agent_results: list[dict]
    reply: str | None
    requires_escalation: bool
```

## Escalation

When an agent sets `requires_escalation: true`, the frontend should notify the user that human intervention may be needed. This is used for complex credit decisions, disputed orders, or low-confidence responses.
