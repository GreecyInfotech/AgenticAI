# Smart Port AI Platform — UML Design Artifacts

End-to-end UML design package for the Smart Port AI Platform. All diagrams are authored in **PlantUML** (`.puml`) and can be rendered to PNG/SVG/PDF.

## Artifact Index

| # | File | UML Type | Scope |
|---|------|----------|-------|
| 01 | [01-system-context.puml](./01-system-context.puml) | C4 / Context | External actors & system boundary |
| 02 | [02-container-diagram.puml](./02-container-diagram.puml) | Container | Major runtime containers |
| 03 | [03-component-diagram.puml](./03-component-diagram.puml) | Component | Internal gateway & agent structure |
| 04 | [04-deployment-diagram.puml](./04-deployment-diagram.puml) | Deployment | K8s / GCP production topology |
| 05 | [05-use-case-diagram.puml](./05-use-case-diagram.puml) | Use Case | Actor goals & system capabilities |
| 06 | [06-domain-class-diagram.puml](./06-domain-class-diagram.puml) | Class | Core domain entities & relationships |
| 07 | [07-sequence-authentication.puml](./07-sequence-authentication.puml) | Sequence | JWT / SSO login flow |
| 08 | [08-sequence-agent-invoke.puml](./08-sequence-agent-invoke.puml) | Sequence | Single-agent AI invocation |
| 09 | [09-sequence-orchestration.puml](./09-sequence-orchestration.puml) | Sequence | Multi-agent workflow |
| 10 | [10-sequence-rag-pipeline.puml](./10-sequence-rag-pipeline.puml) | Sequence | Document ingestion & retrieval |
| 11 | [11-sequence-ml-prediction.puml](./11-sequence-ml-prediction.puml) | Sequence | ML inference flow |
| 12 | [12-sequence-event-flow.puml](./12-sequence-event-flow.puml) | Sequence | Kafka event publish & consume |
| 13 | [13-activity-vessel-arrival.puml](./13-activity-vessel-arrival.puml) | Activity | Vessel arrival business process |
| 14 | [14-activity-customs-clearance.puml](./14-activity-customs-clearance.puml) | Activity | Customs clearance workflow |
| 15 | [15-state-vessel-call.puml](./15-state-vessel-call.puml) | State Machine | Vessel call lifecycle |
| 16 | [16-state-customs-declaration.puml](./16-state-customs-declaration.puml) | State Machine | Declaration lifecycle |
| 17 | [17-package-diagram.puml](./17-package-diagram.puml) | Package | Monorepo module structure |
| 18 | [18-component-security.puml](./18-component-security.puml) | Component | Security & identity layer |

## How to Render

### VS Code / Cursor
Install the **PlantUML** extension, then open any `.puml` file and press `Alt+D` to preview.

### Command Line (Java + PlantUML JAR)
```bash
# Install PlantUML, then:
plantuml docs/uml/*.puml
# Output: PNG files alongside each .puml
```

### Docker
```bash
docker run -v "%cd%/docs/uml:/data" plantuml/plantuml /data/*.puml
```

### Online
Paste file contents into https://www.plantuml.com/plantuml/uml/

## Diagram Relationships

```
01 System Context
    └── 02 Container Diagram
            ├── 03 Component Diagram
            ├── 04 Deployment Diagram
            └── 18 Security Component
05 Use Case Diagram
    ├── 07–12 Sequence Diagrams
    ├── 13–14 Activity Diagrams
    └── 15–16 State Machines
06 Domain Class Diagram  ←→  All operational flows
17 Package Diagram       ←→  Source code structure
```

## Related Documentation

- [Architecture Overview](./architecture.md)
- [API Reference](./api-reference.md)
- [User Manual](./usermanual.md)
- [Deployment Guide](./deployment-guide.md)
