.PHONY: install lint format typecheck test run docker-up docker-down docker-prod helm-lint helm-deploy terraform-plan-dev

install:
	pip install -e ".[dev]"

lint:
	ruff check ai-platform shared gateway tests
	black --check ai-platform shared gateway tests

format:
	ruff check --fix ai-platform shared gateway tests
	black ai-platform shared gateway tests

typecheck:
	mypy ai-platform shared gateway

test:
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -v --cov=ai-platform --cov=shared -p pytest_asyncio.plugin

run:
	uvicorn ai_platform.main:app --host 0.0.0.0 --port 8000 --reload

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

docker-build:
	docker build -f infrastructure/docker/Dockerfile.ai-platform -t ai-platform:latest .
	docker build -f infrastructure/docker/Dockerfile.gateway -t gateway:latest .
	docker build -f infrastructure/docker/Dockerfile.frontend -t frontend:latest .

helm-lint:
	helm lint infrastructure/helm/distributor-platform -f infrastructure/helm/distributor-platform/values-dev.yaml

helm-deploy:
	helm upgrade --install distributor-platform infrastructure/helm/distributor-platform -f infrastructure/helm/distributor-platform/values-dev.yaml --namespace distributor --create-namespace

terraform-plan-dev:
	cd infrastructure/terraform/environments/dev && terraform init -backend=false && terraform plan
