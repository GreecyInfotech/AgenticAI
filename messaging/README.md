# Messaging Platform

Event-driven messaging for orchestration, audit, notifications, and search indexing.

## Modules

| Module | Purpose |
|--------|---------|
| `event-common` | `PlatformEvent`, topic names, event types |
| `kafka-client` | Spring Boot Kafka publisher with NoOp fallback |
| `messaging-api` | Registry + consumer service on port **8550** |

## Topics

| Topic | Purpose |
|-------|---------|
| `bfsi.orchestration.events` | Orchestration lifecycle |
| `bfsi.agent.decisions` | Agent decision stream |
| `bfsi.audit.events` | Audit log events |
| `bfsi.notification.events` | Notification requests |
| `bfsi.search.index` | Search index pipeline |

## Run

```bash
docker compose up -d kafka zookeeper
mvn package -DskipTests -pl messaging/messaging-api -am
KAFKA_ENABLED=true java -jar messaging/messaging-api/target/messaging-api-0.1.0-SNAPSHOT.jar
```

Via API Gateway: `GET http://localhost:8000/api/messaging/topics`

## Configuration

```env
MESSAGING_PORT=8550
KAFKA_ENABLED=false
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

Set `KAFKA_ENABLED=true` when Kafka is running. When disabled, events are logged but not published.
