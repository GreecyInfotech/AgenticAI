# Production Deployment Guide

End-to-end deployment using Docker, Terraform (Azure), and Helm.

## Architecture

```
Terraform (Azure)          Helm (AKS)
├── Resource Group    →    ├── AI Platform
├── VNet + Subnets         ├── Gateway
├── AKS Cluster            ├── Frontend
├── Azure Container Registry ├── Microservices (9)
├── PostgreSQL Flexible    ├── Ingress + TLS
├── Redis Cache            └── HPA autoscaling
├── Event Hubs (Kafka)
└── Key Vault
```

## 1. Docker (Local / VM)

### Development

```bash
docker compose up -d
```

### Production overlay

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Build images

```bash
docker build -f infrastructure/docker/Dockerfile.ai-platform -t ai-platform:0.1.0 .
docker build -f infrastructure/docker/Dockerfile.gateway -t gateway:0.1.0 .
docker build -f infrastructure/docker/Dockerfile.frontend -t frontend:0.1.0 .
```

Production Dockerfiles include:
- Multi-stage builds (AI platform)
- Non-root user (UID 10001)
- Health checks on all services
- Resource limits via `docker-compose.prod.yml`

## 2. Terraform (Azure)

### Prerequisites

- Azure CLI logged in (`az login`)
- Terraform >= 1.6
- Remote state storage account (prod backend)

### Dev environment

```bash
cd infrastructure/terraform/environments/dev
terraform init
terraform plan
terraform apply
```

### Prod environment

```bash
cd infrastructure/terraform/environments/prod
# Edit backend block in main.tf with your state storage
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

### Modules

| Module | Resources |
|--------|-----------|
| `resource_group` | Azure Resource Group |
| `networking` | VNet, subnets, Postgres private DNS |
| `container_registry` | Azure Container Registry |
| `aks` | AKS cluster + Log Analytics + ACR pull |
| `key_vault` | Key Vault with RBAC for AKS |
| `postgres` | PostgreSQL Flexible Server 16 |
| `redis` | Azure Cache for Redis |
| `event_hubs` | Event Hubs namespace + platform topics |

### Outputs for Helm

```bash
terraform output -json helm_external_services
```

## 3. Helm (Kubernetes)

### Install

```bash
# Dev
helm upgrade --install distributor-platform \
  infrastructure/helm/distributor-platform \
  -f infrastructure/helm/distributor-platform/values-dev.yaml \
  --namespace distributor --create-namespace

# Production
helm upgrade --install distributor-platform \
  infrastructure/helm/distributor-platform \
  -f infrastructure/helm/distributor-platform/values.yaml \
  -f infrastructure/helm/distributor-platform/values-prod.yaml \
  --namespace distributor --create-namespace \
  --set global.imageRegistry=<acr-login-server> \
  --set externalServices.postgres.host=<postgres-fqdn> \
  --set externalServices.redis.host=<redis-host> \
  --set externalServices.kafka.bootstrapServers=<event-hubs-endpoint>
```

### Chart features

- Deployments + Services for AI platform, gateway, frontend, 9 microservices
- ConfigMap for shared environment
- Secrets for JWT, OpenAI key, DB passwords
- Ingress with TLS (cert-manager)
- HorizontalPodAutoscaler for AI platform and gateway
- Pod security context (non-root)
- Anti-affinity rules (prod)

### Validate

```bash
helm lint infrastructure/helm/distributor-platform
helm template distributor-platform infrastructure/helm/distributor-platform -f infrastructure/helm/distributor-platform/values-dev.yaml
```

## 4. Full Production Pipeline

```bash
# 1. Provision infrastructure
cd infrastructure/terraform/environments/prod && terraform apply

# 2. Configure kubectl
az aks get-credentials --resource-group rg-distributor-platform-prod --name aks-distributor-platform-prod

# 3. Build and push images to ACR
ACR=$(terraform output -raw acr_login_server)
docker build -f infrastructure/docker/Dockerfile.ai-platform -t $ACR/ai-platform:0.1.0 .
docker push $ACR/ai-platform:0.1.0
# ... repeat for gateway, frontend, microservices

# 4. Deploy Helm chart
helm upgrade --install distributor-platform infrastructure/helm/distributor-platform \
  -f infrastructure/helm/distributor-platform/values-prod.yaml \
  --namespace distributor --create-namespace

# 5. Verify
kubectl get pods -n distributor
kubectl get ingress -n distributor
```

## Security Checklist

- [ ] Store secrets in Azure Key Vault (not Helm values)
- [ ] Use `secrets.create: false` in prod Helm values
- [ ] Enable private endpoints for Postgres and Redis
- [ ] Restrict `allowed_ingress_cidrs` in Terraform
- [ ] Rotate JWT secret and API keys regularly
- [ ] Enable Azure Policy on AKS
