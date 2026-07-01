#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHART="${ROOT}/infrastructure/helm/distributor-platform"
RELEASE="${RELEASE:-distributor-platform}"
NAMESPACE="${NAMESPACE:-distributor}"
VALUES="${VALUES:-${CHART}/values-dev.yaml}"

helm lint "${CHART}" -f "${VALUES}"
helm upgrade --install "${RELEASE}" "${CHART}" \
  -f "${VALUES}" \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  "$@"

echo "Deployed ${RELEASE} to namespace ${NAMESPACE}"
