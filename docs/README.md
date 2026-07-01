# Documentation Index

Complete documentation for the **AI Distributor Ordering Platform**.

## Getting Started

| Document | Description |
|----------|-------------|
| [User Manual](usermanual.md) | Setup, configuration, folder reference, troubleshooting |
| [Frontend Guide](frontend.md) | React web app development and usage |

## Architecture

| Document | Description |
|----------|-------------|
| [Overview](architecture/overview.md) | High-level architecture and design principles |
| [System Design](architecture/system-design.md) | Components, data flow, technology stack |

## Sequence Diagrams

| Document | Description |
|----------|-------------|
| [Order Flow](sequence-diagrams/order-flow.md) | Order placement end-to-end |
| [Conversation Flow](sequence-diagrams/conversation-flow.md) | AI agent orchestration flow |

## API Reference

| Document | Description |
|----------|-------------|
| [REST API](api/rest-api.md) | All HTTP endpoints with examples |
| [Authentication](api/authentication.md) | JWT auth, roles, permissions |
| [Kafka Events](api/events.md) | Event schemas and topics |

## Deployment

| Document | Description |
|----------|-------------|
| [Local Development](deployment/local.md) | Run backend + frontend locally |
| [Docker Compose](deployment/docker.md) | Full stack with containers |
| [Production](deployment/production.md) | Production checklist and hardening |

## Operations

| Document | Description |
|----------|-------------|
| [Service Health](runbooks/service-health.md) | Health checks and dependency monitoring |
| [Incident Response](runbooks/incident-response.md) | Common incidents and remediation |

## Design Decisions

| ADR | Title |
|-----|-------|
| [ADR-001](ADR/001-clean-architecture.md) | Clean Architecture layers |
| [ADR-002](ADR/002-langgraph-orchestration.md) | LangGraph multi-agent orchestration |
| [ADR-003](ADR/003-event-driven-microservices.md) | Kafka event-driven microservices |

## Prompts

| Document | Description |
|----------|-------------|
| [Agent Prompts](prompts/agent-prompts.md) | Agent prompt design and conventions |

## Quick Links

| Resource | URL (local dev) |
|----------|-----------------|
| Frontend | http://localhost:5173 |
| AI Platform API | http://localhost:8000 |
| OpenAPI (Swagger) | http://localhost:8000/docs |
| API Gateway | http://localhost:8080 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
