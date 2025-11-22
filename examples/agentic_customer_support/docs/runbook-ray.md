# Ray Serve Deployment & Validation Runbook

This runbook explains how to package, deploy, and validate the Ray Serve implementation on a Kubernetes cluster with GPU nodes available.

> Part of the [documentation hub](./README.md). Pair it with `runbook-asya.md` for parity checks.

---

## 1. Prerequisites

- Kubernetes cluster with GPU workers
- Ray operator (or Ray on K8s) installed
- Docker/OCI registry for pushing images
- `kubectl`, `docker`, `python`, `ray` CLI available locally

Recommended environment variables:

```bash
export REGISTRY="ghcr.io/<org>/customer-support"
export TAG="v0.1.0"
export NAMESPACE="ray-cs"
export RAY_ENDPOINT="http://<load-balancer-host>:8000/support"
```

---

## 2. Build & Push Ray Serve Image

```bash
cd examples/agentic_customer_support

# Build image from ray_app/Dockerfile
REGISTRY=$REGISTRY TAG=$TAG ./scripts/build_ray_image.sh

# Push to your registry
docker push "${REGISTRY}/${IMAGE_NAME:-ray-serve}:${TAG}"
```

> Update `ray_app/config/example-deployment.yaml` to reference your registry/tag if different from `customer-support/ray-serve:latest`.

---

## 3. Deploy to Kubernetes

```bash
cd examples/agentic_customer_support
NAMESPACE=$NAMESPACE ./scripts/deploy_ray.sh
```

This script:
1. Ensures the namespace exists (`ray_app/config/namespace.yaml`)
2. Applies `ray_app/config/example-deployment.yaml`
3. Displays current pods and services

Watch the pods until they reach `Running`:

```bash
kubectl get pods -n $NAMESPACE -w
```

Expose the service (if LoadBalancer pending, you can port-forward temporarily):

```bash
kubectl port-forward svc/ray-serve-customer-support 8000:8000 -n $NAMESPACE
```

---

## 4. Validate the Deployment

Send a test ticket through the Ray Serve HTTP endpoint:

```bash
python scripts/send_test_ticket.py \
  --framework ray \
  --ticket examples/test_ticket.json \
  --endpoint "$RAY_ENDPOINT"
```

Check that the response includes:

- `status: completed`
- `formatted_response` with intent, urgency, quality score
- No `error` field

Inspect Ray Serve logs if needed:

```bash
kubectl logs deployment/ray-serve-customer-support -n $NAMESPACE
```

For more detail, use `ray dashboard` or Ray CLI to inspect replicas and autoscaling.

---

## 5. Troubleshooting

| Issue | Actions |
|-------|---------|
| Pods CrashLoopBackOff | Ensure image/tag matches the pushed image; confirm Ray operator CRDs exist |
| Service not reachable | Check LoadBalancer provisioning; use port-forward as fallback |
| Requests timeout | Verify `RAY_ENDPOINT`, confirm pods are ready, inspect Ray Serve logs |
| GPU not allocated | Confirm node labels/resources, adjust deployment resources accordingly |

---

## 6. Next Steps

- Capture latency/throughput metrics and update [`comparison.md`](comparison.md)
- Compare resource usage vs Asya deployment
- Feed insights into [`case-study.md`](case-study.md) and any public write-ups

This runbook completes the "Build on Ray Serve – Deploy and validate" milestone by providing a reproducible deployment + validation workflow. Execute it on your Kubernetes cluster to gather empirical data for the comparison study.
