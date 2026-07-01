#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

echo "Building production images..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml build

echo "Starting production stack..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

echo "Waiting for AI platform health..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:8000/api/v1/health >/dev/null; then
    echo "AI platform is UP"
    exit 0
  fi
  sleep 2
done

echo "Health check timed out — check: docker compose logs ai-platform"
exit 1
