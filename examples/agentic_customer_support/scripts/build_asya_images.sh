#!/usr/bin/env bash
set -euo pipefail

# Builds container images for every Asya handler using the shared Dockerfile.
# Usage:
#   REGISTRY=ghcr.io/my-org/customer-support TAG=dev ./scripts/build_asya_images.sh
#
# Defaults build to local "customer-support" namespace for quick testing.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="${REGISTRY:-customer-support}"
TAG="${TAG:-latest}"
DOCKERFILE="${ROOT_DIR}/asya/Dockerfile"

declare -A HANDLERS=(
  ["ticket-ingester"]="handlers.ticket_ingester.process"
  ["intent-classifier"]="handlers.intent_classifier.IntentClassifier.process"
  ["knowledge-retriever"]="handlers.knowledge_retriever.KnowledgeRetriever.process"
  ["response-generator"]="handlers.response_generator.ResponseGenerator.process"
  ["response-validator"]="handlers.response_validator.ResponseValidator.process"
  ["response-formatter"]="handlers.response_formatter.process"
  ["escalation-handler"]="handlers.escalation_handler.process"
)

for IMAGE in "${!HANDLERS[@]}"; do
  HANDLER_PATH="${HANDLERS[$IMAGE]}"
  TARGET_IMAGE="${REGISTRY}/${IMAGE}:${TAG}"
  echo "→ Building ${TARGET_IMAGE} (handler: ${HANDLER_PATH})"
  docker build \
    -f "${DOCKERFILE}" \
    --build-arg HANDLER="${HANDLER_PATH}" \
    -t "${TARGET_IMAGE}" \
    "${ROOT_DIR}/asya"
done

echo "All handler images built with tag: ${TAG}"
