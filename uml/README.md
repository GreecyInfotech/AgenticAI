# UML Artifacts

PlantUML source files for the AI Distributor Ordering Platform.

## Quick View

Open **[UML.md](../UML.md)** in the repository root for Mermaid diagrams (renders on GitHub).

## PlantUML Files

| File | Diagram Type |
|------|--------------|
| `01-system-context.puml` | C4 System Context |
| `02-container.puml` | C4 Container |
| `03-component-ai-platform.puml` | Component |
| `04-class-application.puml` | Class (CQRS) |
| `05-class-infrastructure.puml` | Class (Infrastructure) |
| `06-sequence-conversation.puml` | Sequence |
| `07-sequence-place-order.puml` | Sequence |
| `08-sequence-cancel-order.puml` | Sequence |
| `09-sequence-startup.puml` | Sequence |
| `10-activity-orchestrator.puml` | Activity |
| `11-state-order.puml` | State Machine |
| `12-deployment.puml` | Deployment |

## Render

### VS Code / Cursor

Install the **PlantUML** extension, open any `.puml` file, press `Alt+D`.

### CLI

```bash
java -jar plantuml.jar plantuml/*.puml -o ../output
```

### Online

Paste file contents into [plantuml.com/plantuml](https://www.plantuml.com/plantuml/uml/).
