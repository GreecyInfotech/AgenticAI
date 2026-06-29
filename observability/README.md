# Observability Platform

Production observability stack for the BFSI Agentic AI Platform.

## Components

| Component | Path | Port |
|-----------|------|------|
| Prometheus | `prometheus/prometheus.yml` | 9090 |
| Grafana | `grafana/provisioning/` | 3000 |
| Loki | `loki/loki-config.yml` | 3100 |
| Tempo | `tempo/tempo.yml` | 3200 |
| OpenTelemetry Collector | `opentelemetry/otel-collector-config.yml` | 4317/4318 |
| Java starter | `platform-observability/` | — |

## Java integration

Add to any Spring Boot service:

```xml
<dependency>
    <groupId>com.bfsi.platform</groupId>
    <artifactId>platform-observability</artifactId>
    <version>${project.version}</version>
</dependency>
```

Exposes `/actuator/prometheus` with common `platform=bfsi` tags.

## Start stack

```bash
docker compose up -d prometheus grafana loki tempo
```

Grafana: http://localhost:3000 (admin/admin)

## OpenTelemetry

Point services at the collector:

```env
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=orchestrator
```
