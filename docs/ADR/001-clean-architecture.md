# ADR-001: Clean Architecture

**Status:** Accepted  
**Date:** 2026-07-01  
**Deciders:** Platform Team

## Context

The AI Distributor Ordering Platform has multiple services, agents, and external integrations. We need a consistent architecture that keeps business logic testable, independent of frameworks, and maintainable as the team grows.

## Decision

Adopt **Clean Architecture** with four layers:

1. **Presentation** — API routes, gateway, frontend (HTTP concerns only)
2. **Application** — Use cases, commands, queries, DTOs (orchestration)
3. **Domain** — Entities, repository interfaces, domain services (business rules)
4. **Infrastructure** — Database, Kafka, Redis, external API adapters (implementations)

### Dependency Rule

Dependencies point inward only:

```
Presentation → Application → Domain ← Infrastructure
```

Domain entities must not import FastAPI, LangGraph, or database drivers.

## Consequences

### Positive

- Business logic is testable without HTTP or database
- Repository interfaces allow swapping Postgres for in-memory in tests
- New integrations (ERP, CRM) only touch infrastructure layer
- Agents call tools, not repositories directly

### Negative

- More files and indirection for simple CRUD operations
- Requires discipline to prevent layer violations
- DTO mapping adds boilerplate between API and domain

## Implementation

- Domain interfaces: `ai-platform/ai_platform/domain/*/repository.py`
- Implementations: `ai-platform/ai_platform/infrastructure/repositories/`
- Use cases: `ai-platform/ai_platform/application/use_cases/`
- API handlers call use cases, never repositories directly

## References

- `.cursor/rules/architecture.mdc`
- `docs/architecture/system-design.md`
