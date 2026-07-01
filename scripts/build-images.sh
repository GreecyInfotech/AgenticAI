#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="${REGISTRY:-ghcr.io/greecyinfotech/agenticai}"
TAG="${TAG:-0.1.0}"

cd "${ROOT}"

echo "Building core images (${REGISTRY}, tag ${TAG})..."
docker build -f infrastructure/docker/Dockerfile.ai-platform -t "${REGISTRY}/ai-platform:${TAG}" .
docker build -f infrastructure/docker/Dockerfile.gateway -t "${REGISTRY}/gateway:${TAG}" .
docker build -f infrastructure/docker/Dockerfile.frontend -t "${REGISTRY}/frontend:${TAG}" .

SERVICES=(
  order-service inventory-service customer-service pricing-service
  payment-service shipment-service promotion-service notification-service analytics-service
)

for svc in "${SERVICES[@]}"; do
  echo "Building ${svc}..."
  docker build \
    -f infrastructure/docker/Dockerfile.service \
    --build-arg "SERVICE_NAME=${svc}" \
    -t "${REGISTRY}/microservice-${svc}:${TAG}" \
    .
done

echo "All images built. Push with: docker push ${REGISTRY}/<image>:${TAG}"
