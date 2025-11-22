#!/usr/bin/env bash
set -euo pipefail

# Builds the Ray Serve container image located in ray_app/.
# Usage:
#   REGISTRY=ghcr.io/my-org/customer-support TAG=v0.1.0 ./scripts/build_ray_image.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="${ROOT_DIR}/ray_app"
DOCKERFILE="${APP_DIR}/Dockerfile"
REGISTRY="${REGISTRY:-customer-support}"
IMAGE_NAME="${IMAGE_NAME:-ray-serve}"
TAG="${TAG:-latest}"
TARGET_IMAGE="${REGISTRY}/${IMAGE_NAME}:${TAG}"

echo "→ Building ${TARGET_IMAGE}"
docker build -f "${DOCKERFILE}" -t "${TARGET_IMAGE}" "${APP_DIR}"

echo "Image built: ${TARGET_IMAGE}"
