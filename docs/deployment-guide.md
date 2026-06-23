# Deployment Guide

## Local Development

```bash
cp .env.example .env
make infra-up    # Start postgres, kafka, redis, monitoring
make install     # Install dependencies
make dev         # Start all services
```

## Docker Compose

Full stack with all services:

```bash
docker compose up -d
docker compose logs -f api-gateway
```

Selective services:

```bash
docker compose up -d postgres redis kafka api-gateway vessel-agent port-operations-ui
```

## Kubernetes

### Prerequisites

- GKE cluster (or any Kubernetes 1.28+)
- kubectl configured
- Helm 3.x

### Deploy

```bash
# Create namespace and base resources
kubectl apply -f deployment/kubernetes/base/

# Install Helm chart
helm upgrade --install smart-port deployment/helm/smart-port/ \
  -n smart-port --create-namespace \
  -f deployment/helm/smart-port/values.yaml

# Verify
kubectl get pods -n smart-port
```

### Agent Deployment

Use the agent template for each agent:

```bash
for agent in vessel container customs; do
  sed "s/AGENT_NAME/${agent}-agent/g; s/AGENT_PORT/810x/g" \
    deployment/kubernetes/agents/agent-template.yaml | kubectl apply -f -
done
```

## Terraform (GCP)

```bash
cd deployment/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your project_id

terraform init
terraform plan
terraform apply
```

Resources created:
- GKE cluster with autoscaling node pool
- Cloud SQL PostgreSQL 16 with pgvector
- Cloud Storage buckets (documents, ML models, backups)
- BigQuery analytics dataset
- Memorystore Redis
- VPC networking

## Cloud Run

For serverless deployment of individual services:

```bash
gcloud run deploy api-gateway \
  --image smart-port/api-gateway:latest \
  --port 8080 \
  --min-instances 1 \
  --max-instances 10
```

See `deployment/cloudrun/services.yaml` for full service definitions.

## CI/CD

GitHub Actions workflow at `.github/workflows/ci-cd.yml`:

1. **Lint** — Python (ruff) and TypeScript
2. **Test** — pytest and Jest
3. **Build** — Docker images pushed to GHCR
4. **Deploy** — Staging via kubectl + Helm

Required secrets:
- `GCP_SA_KEY` — GCP service account JSON
- `GITHUB_TOKEN` — Auto-provided for GHCR

## Environment Variables

See `.env.example` for all configuration options. Critical production variables:

| Variable | Description |
|----------|-------------|
| JWT_SECRET | JWT signing secret (required) |
| OPENAI_API_KEY | OpenAI API key for agents |
| POSTGRES_PASSWORD | Database password |
| OKTA_DOMAIN | Okta SSO domain |
| AZURE_AD_TENANT_ID | Azure AD tenant |

## Monitoring

After deployment, access:
- Grafana: Configure Prometheus datasource (auto-provisioned)
- Prometheus: Scrapes all service health endpoints
- OpenTelemetry: Traces exported to OTEL collector

Alert rules defined in `observability/alerting/rules.yml`.
