.PHONY: install lint format typecheck test run docker-up docker-down

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
