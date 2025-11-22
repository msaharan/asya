#!/usr/bin/env bash
set -euo pipefail

# Applies the example Ray Serve deployment manifests into a Kubernetes cluster.
# Requires the Ray operator (or equivalent resources) to be available.
#
# Usage:
#   NAMESPACE=ray-cs ./scripts/deploy_ray.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="${ROOT_DIR}/ray_app"
NAMESPACE="${NAMESPACE:-ray-cs}"
NAMESPACE_MANIFEST="${APP_DIR}/config/namespace.yaml"
MANIFEST="${APP_DIR}/config/example-deployment.yaml"

echo "→ Ensuring namespace '${NAMESPACE}' exists"
kubectl apply -f <(sed "s/name: ray-cs/name: ${NAMESPACE}/" "${NAMESPACE_MANIFEST}")

echo "→ Deploying Ray Serve resources into namespace '${NAMESPACE}'"
kubectl apply -n "${NAMESPACE}" -f "${MANIFEST}"

echo "→ Current pods:"
kubectl get pods -n "${NAMESPACE}"

echo "→ Services:"
kubectl get svc -n "${NAMESPACE}"

echo "Ray Serve deployment applied. Use scripts/send_test_ticket.py --framework ray to validate."
