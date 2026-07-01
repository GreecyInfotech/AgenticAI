# Agent Prompt Design

Conventions and guidelines for LLM prompts used by the 14 specialist agents.

## Prompt Structure

Each agent has a `prompt.py` that builds the prompt from typed input:

```python
def build_prompt(input_data: CustomerAgentInput) -> str:
    return (
        "You are the customer agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
```

## Agent Module Contract

Every agent under `ai-platform/ai_platform/agents/{name}_agent/` must include:

| File | Purpose |
|------|---------|
| `agent.py` | Agent executor — calls LLM, returns typed output |
| `prompt.py` | Prompt builder (will migrate to Jinja2 templates) |
| `schemas.py` | `Input` and `Output` Pydantic models with confidence score |
| `state.py` | LangGraph TypedDict state |
| `tools.py` | Tool definitions for LLM function calling |
| `memory.py` | Session memory wrapper |
| `tests.py` | Smoke tests (no real LLM calls) |

## Output Schema

All agents return outputs with:

```python
class AgentOutput(BaseModel):
    agent: str
    message: str
    confidence: float = Field(ge=0.0, le=1.0)
    data: dict = Field(default_factory=dict)
    requires_escalation: bool = False
```

## Prompt Rules

Per `.cursor/rules/prompt-engineering.mdc`:

1. **Templates in `prompts/`** — system prompts in `prompts/system/`, domain prompts in `prompts/<domain>/`
2. **Jinja2** — use `prompts/templates/` for variable substitution
3. **Few-shot examples** — versioned per agent in `prompts/few_shots/`
4. **No PII or secrets** in prompt templates
5. **RAG context** injected via `prompts/rag/` templates with citation placeholders
6. **Token limit** — keep prompts under 4000 tokens; summarize long context

## The 14 Agents

| Agent | System Role | Key Context |
|-------|------------|-------------|
| supervisor_agent | Route to specialist | User message, session history |
| customer_agent | Customer profiles | Customer ID, account tier |
| inventory_agent | Stock availability | SKU, warehouse, quantities |
| pricing_agent | Price quotes | SKU, quantity, customer tier |
| promotion_agent | Promotions/coupons | Campaign rules, eligibility |
| credit_agent | Credit limits | Customer credit profile |
| order_agent | Order placement | Cart items, validation rules |
| shipment_agent | Tracking/logistics | Order ID, carrier info |
| payment_agent | Payment status | Invoice, payment terms |
| recommendation_agent | Product suggestions | Purchase history, catalog |
| notification_agent | Email/SMS | Templates, recipient |
| analytics_agent | Reporting | Sales data, KPIs |
| document_agent | Invoices/docs | Order details, templates |
| knowledge_agent | FAQ/RAG | Knowledge base retrieval |

## RAG Integration

Knowledge agent and domain agents can receive RAG context:

```
prompts/rag/
├── context_template.j2    # Wraps retrieved chunks with citations
└── citation_format.j2     # [Source: {doc_id}] format
```

Retrieval pipeline: `ai-platform/ai_platform/rag/pipelines/retrieval_pipeline.py`

## Guardrails

- **Input:** `is_prompt_injection()` check before sending to LLM
- **Output:** `llm/guardrails.py` validates response format and content
- **PII:** Never include customer PII in prompts sent to external LLMs without masking

## Future: Jinja2 Migration

Current prompts are f-string based. Planned migration:

```
prompts/
├── system/
│   └── base.j2
├── order/
│   └── place_order.j2
├── few_shots/
│   └── order_agent_v1.json
└── templates/
    └── agent_wrapper.j2
```

## Related

- `.cursor/rules/prompt-engineering.mdc`
- `.cursor/rules/ai-agent.mdc`
- `docs/sequence-diagrams/conversation-flow.md`
