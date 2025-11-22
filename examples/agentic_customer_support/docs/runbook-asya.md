# Asya Deployment & Validation Runbook

This guide describes how to build, deploy, and validate the Asya implementation on a Kubernetes cluster that already has the Asya operator and transport configured.

> Part of the [documentation hub](./README.md). Pair it with `runbook-ray.md` for side-by-side ops.

---

## 1. Prerequisites

- Kubernetes cluster with GPU nodes, reachable via `kubectl`
- Asya operator installed (see official docs)
- Transport configured (SQS or RabbitMQ) with credentials injected into the operator
- Docker/OCI registry you can push images to (e.g. GHCR, ECR)
- `kubectl`, `docker`, and `python` available locally

Set the following environment variables to avoid repeating flags:

```bash
export REGISTRY="ghcr.io/<org>/customer-support"
export TAG="v0.1.0"
export NAMESPACE="asya-cs"
export ASYA_GATEWAY_URL="https://<gateway-host>/envelopes"
```

---

## 2. Build & Push Handler Images

```bash
cd examples/agentic_customer_support

# Build all handler images
REGISTRY=$REGISTRY TAG=$TAG ./scripts/build_asya_images.sh

# Push to your registry
for image in ticket-ingester intent-classifier knowledge-retriever \
             response-generator response-validator response-formatter \
             escalation-handler; do
  docker push "${REGISTRY}/${image}:${TAG}"
done
```

> Update `asya/config/example-asyncactor.yaml` if your registry/tag differs from the defaults (`customer-support/<handler>:latest`).

---

## 3. Deploy AsyncActors

```bash
cd examples/agentic_customer_support
NAMESPACE=$NAMESPACE ./scripts/deploy_asya.sh
```

This script:
1. Ensures the namespace exists (`asya/config/namespace.yaml`)
2. Applies `asya/config/example-asyncactor.yaml`
3. Prints current AsyncActors and pods for quick inspection

You can watch the rollout:

```bash
kubectl get pods -n $NAMESPACE -w
```

---

## 4. Validate the Pipeline

1. Confirm all pods are `Running` and `READY`.
2. Send a test ticket through the Asya gateway:

```bash
python scripts/send_test_ticket.py \
  --framework asya \
  --ticket examples/test_ticket.json \
  --endpoint "$ASYA_GATEWAY_URL"
```

3. Verify the response includes:
   - `status: completed`
   - `formatted_response` with intent, urgency, sources
   - `judge_score` >= 0.7 (or `needs_refinement: true` if below threshold)

4. Check logs for each actor:

```bash
kubectl logs deployment/ticket-ingester -n $NAMESPACE
kubectl logs deployment/intent-classifier -n $NAMESPACE
# ...repeat for other actors
```

---

## 5. Troubleshooting Checklist

| Symptom | Checks |
|---------|--------|
| Pods CrashLoopBackOff | Ensure images point to the registry/tag you pushed; confirm `REGISTRY/TAG` edits in AsyncActor spec |
| Queue errors | Verify transport credentials/secrets were mounted; inspect sidecar logs |
| Gateway 5xx | Confirm gateway points at the correct namespace/queue; inspect gateway pod logs |
| Messages stuck after validation | Check for `needs_refinement` flag; ensure downstream actors (formatter/escalation) are running |

---

## 6. Next Steps

- Capture metrics (latency, throughput) and record them in [`comparison.md`](comparison.md)
- Update [`case-study.md`](case-study.md) with real results
- Export Kubernetes manifests or helm charts if you want reproducible CI/CD deployments

This runbook satisfies the "Build on Asya - Deploy and validate" milestone by providing a reproducible path from source to a working Asya deployment. Actual cluster execution should use these steps and archive logs/metrics for the comparison study.
