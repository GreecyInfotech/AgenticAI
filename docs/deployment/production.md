# Production Deployment

This guide covers Docker, Terraform (Azure), and Helm deployment for production.

For the full reference, see [infrastructure/README.md](../../infrastructure/README.md).

## Quick Start

### Docker (single host)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Azure infrastructure

```bash
cd infrastructure/terraform/environments/prod
terraform init
terraform apply -var-file=terraform.tfvars
```

### Kubernetes (Helm)

```bash
helm upgrade --install distributor-platform infrastructure/helm/distributor-platform \
  -f infrastructure/helm/distributor-platform/values-prod.yaml \
  --namespace distributor --create-namespace
```

## Makefile targets

| Target | Description |
|--------|-------------|
| `make docker-prod` | Start production Docker Compose stack |
| `make docker-build` | Build core Docker images |
| `make helm-lint` | Lint Helm chart |
| `make helm-deploy` | Deploy chart to dev namespace |
| `make terraform-plan-dev` | Plan dev Terraform (local state) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/build-images.sh` | Build all container images |
| `scripts/deploy-docker-prod.sh` | Build + start prod compose with health check |
| `scripts/deploy-helm.sh` | Lint and install Helm release |

## CI/CD

- **`.github/workflows/docker.yml`** — builds and pushes images to GHCR on branch push
- **`.github/workflows/deploy-prod.yml`** — Helm deploy to AKS on version tags (`v*.*.*`)

Required GitHub secrets for prod deploy:

- `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`
- `AKS_RESOURCE_GROUP`, `AKS_CLUSTER_NAME`
- `ACR_LOGIN_SERVER`, `POSTGRES_HOST`, `REDIS_HOST`, `KAFKA_BOOTSTRAP`

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Terraform  │────▶│  AKS + ACR   │────▶│  Helm Chart     │
│  (Azure)    │     │              │     │  (apps + Qdrant)│
└─────────────┘     └──────────────┘     └─────────────────┘
      │                                           │
      ├── PostgreSQL Flexible                     ├── AI Platform
      ├── Redis Cache                             ├── Gateway + Frontend
      ├── Event Hubs (Kafka)                      └── 9 Microservices
      └── Key Vault
```
