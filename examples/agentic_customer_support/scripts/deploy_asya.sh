#!/usr/bin/env bash
set -euo pipefail

# Simple helper for deploying all AsyncActors into a Kubernetes cluster that
# already has the Asya operator installed and transport configured.
#
# Usage:
#   NAMESPACE=asya-cs ./scripts/deploy_asya.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAMESPACE="${NAMESPACE:-asya-cs}"
MANIFEST="${ROOT_DIR}/asya/config/example-asyncactor.yaml"
NAMESPACE_MANIFEST="${ROOT_DIR}/asya/config/namespace.yaml"

echo "→ Ensuring namespace '${NAMESPACE}' exists"
kubectl apply -f <(sed "s/name: asya-cs/name: ${NAMESPACE}/" "${NAMESPACE_MANIFEST}")

echo "→ Deploying AsyncActors into namespace '${NAMESPACE}'"
kubectl apply -n "${NAMESPACE}" -f "${MANIFEST}"

echo "→ Current AsyncActor resources:"
kubectl get asyncactors -n "${NAMESPACE}"

echo "→ Pods:"
kubectl get pods -n "${NAMESPACE}"

echo "Asya handlers deployed. Use scripts/send_test_ticket.py to validate via the gateway."
