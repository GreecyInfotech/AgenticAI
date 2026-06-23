# Smart Port AI Platform - Makefile

.PHONY: help install dev infra-up infra-down build test lint clean scaffold

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	pnpm install
	uv sync

scaffold: ## Regenerate service scaffolds
	python scripts/scaffold_services.py
	python scripts/scaffold_frontends.py

infra-up: ## Start infrastructure (postgres, kafka, redis, monitoring)
	docker compose up -d postgres redis kafka zookeeper schema-registry elasticsearch prometheus grafana otel-collector

infra-down: ## Stop infrastructure
	docker compose down

dev: infra-up ## Start full development stack
	docker compose up -d

dev-gateways: ## Start gateways only (local dev)
	pnpm dev:api-gateway &
	pnpm dev:agent-gateway

build: ## Build all Docker images
	docker compose build

build-ts: ## Build TypeScript packages
	pnpm build

test: ## Run all tests
	uv run pytest agents/ -v --tb=short
	pnpm test

test-python: ## Run Python tests
	uv run pytest agents/vessel-agent/tests/ -v

lint: ## Run linters
	uv run ruff check agents/ mcp-servers/ rag/ ml-platform/ shared/python/
	uv run ruff format --check agents/ mcp-servers/ rag/ ml-platform/
	pnpm lint

format: ## Auto-format code
	uv run ruff format agents/ mcp-servers/ rag/ ml-platform/ shared/python/

clean: ## Remove build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true

terraform-plan: ## Plan Terraform deployment
	cd deployment/terraform && terraform plan -var-file=terraform.tfvars

terraform-apply: ## Apply Terraform deployment
	cd deployment/terraform && terraform apply -var-file=terraform.tfvars

helm-install: ## Install Helm chart
	helm upgrade --install smart-port deployment/helm/smart-port/ -n smart-port --create-namespace

k8s-apply: ## Apply Kubernetes manifests
	kubectl apply -f deployment/kubernetes/base/
