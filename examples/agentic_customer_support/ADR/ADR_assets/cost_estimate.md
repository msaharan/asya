# Cost Estimate: Agentic Customer Support on Amazon EKS

This document provides rough, order-of-magnitude cost estimates for running the `agentic_customer_support` example on Amazon EKS in `us-east-1`, in two configurations:

- CPU-only cluster (cheaper, for learning and basic experiments)
- GPU-backed cluster (closer to a realistic LLM deployment)

These estimates assume:

- Short-lived experiments (hours to a few days), not 24/7 production
- Default EKS pricing and approximate EC2 instance prices as of 2025
- Light traffic and modest logging

Always check the AWS pricing pages for up-to-date numbers.

---

## 1. Shared Assumptions

- **Region**: `us-east-1`
- **EKS version**: 1.30 (any supported 1.2x+ is fine)
- **Cluster**: 1 EKS control plane, 1 managed node group
- **Node volume**: 50–100 GiB gp3 per node
- **Traffic**: Low request volume for experimentation
- **Workloads**:
  - Asya operator, KEDA
  - Asya gateway + crew
  - Asya `agentic_customer_support` handlers (AsyncActors)
  - Ray Serve `agentic_customer_support` app (Ray head + workers)

The intent of the example is to run **both Asya and Ray Serve on the same Kubernetes cluster** and compare them. The cost tables assume that Asya and Ray share the same cluster and nodegroup; you only add more cost if you scale out to more or larger nodes.

The example is not a constant high-throughput workload, so SQS/S3/network costs are assumed to be negligible relative to EC2/EKS.

---

## 2. CPU-Only Cluster (Cheaper, Recommended First)

**Cluster shape (example)**:

- EKS control plane: 1 cluster
- Node group:
  - Instance type: `t3.large` (2 vCPU, 8 GiB RAM)
  - Nodes: 1 (min) – 2 (max), assume **1 node** active for estimates
  - Volume: 50 GiB gp3

### 2.1 Hourly and Daily Cost (Approximate)

| Component         | Unit price (approx.) | Quantity  | Cost/hour   | Cost/day (24h) |
| ----------------- | -------------------- | --------- | ----------- | -------------- |
| EKS control plane | \$0.10 per hour      | 1 cluster | \$0.10      | \$2.40         |
| EC2 `t3.large`    | \$0.083 per hour     | 1 node    | \$0.083     | \$1.99         |
| EBS 50 GiB (gp3)  | \$0.08 per GB-month  | 50 GiB    | ~\$0.005    | ~\$0.12        |
| **Subtotal**      |                      |           | **~\$0.19** | **~\$4.50**    |

For short experiments (e.g. a 4–6 hour session in a single day), total cost is typically:

- **4 hours**: ~\$0.19 × 4 ≈ **\$0.75**
- **6 hours**: ~\$0.19 × 6 ≈ **\$1.15**

Plus pennies for S3/SQS/CloudWatch.

### 2.2 Monthly 24/7 Cost (Not Recommended for Experiments)

If you left this small cluster running continuously for a full 30-day month:

- Hourly subtotal ~\$0.19 × 24 × 30 ≈ **\$136/month**

For learning and evaluation, it is better to:

- Spin the cluster up when you need it
- Delete the cluster when you are done

---

## 3. GPU-Backed Cluster (Closer to “Real” LLM Setup)

**Cluster shape (example)**:

- EKS control plane: 1 cluster
- Node group:
  - Instance type: `g4dn.xlarge` (4 vCPU, 16 GiB RAM, 1 GPU)
  - Nodes: 1 (min) – 2 (max), assume **1 GPU node** active
  - Volume: 100 GiB gp3

### 3.1 Hourly and Daily Cost (Approximate)

| Component         | Unit price (approx.)     | Quantity  | Cost/hour   | Cost/day (24h) |
| ----------------- | ------------------------ | --------- | ----------- | -------------- |
| EKS control plane | \$0.10 per hour          | 1 cluster | \$0.10      | \$2.40         |
| EC2 `g4dn.xlarge` | \$0.75 per hour (approx) | 1 node    | \$0.75      | \$18.00        |
| EBS 100 GiB (gp3) | \$0.08 per GB-month      | 100 GiB   | ~\$0.01     | ~\$0.24        |
| **Subtotal**      |                          |           | **~\$0.86** | **~\$20.60**   |

Short experiment windows:

- **2 hours**: ~\$0.86 × 2 ≈ **\$1.70**
- **4 hours**: ~\$0.86 × 4 ≈ **\$3.40**

Again, S3/SQS/CloudWatch add only cents at low volume.

### 3.2 Monthly 24/7 Cost (Production-Style, Not for Hackathons)

If left running continuously for 30 days:

- ~\$0.86 × 24 × 30 ≈ **\$619/month**

This is why GPU clusters should only be kept up when actively needed during an experiment.

---

## 4. Ray Serve on the Same Cluster

Ray Serve runs as a set of pods (Ray head + worker pods) in the same EKS cluster. From a cost perspective:

- If Asya and Ray share the same nodegroup and you keep total resource usage within the capacity of a single node, there is **no additional EC2/EKS line item** for Ray Serve beyond:
  - Higher CPU/GPU utilization on that node
  - Slightly more CloudWatch logging and network traffic
- If you dedicate **separate nodes** or a separate nodegroup to Ray Serve (for isolation or performance), you can treat that as “doubling” the node cost:
  - CPU-only comparison: add another `t3.large` node (≈ \$0.083/hr).
  - GPU comparison: add another `g4dn.xlarge` node (≈ \$0.75/hr).

For a fair comparison under a tight budget, the typical pattern is:

- Use **one small nodegroup** and schedule both Asya and Ray pods on it (CPU-only first).
- Run **short benchmarks** (minutes to a couple of hours).
- Tear the cluster down afterward.

This keeps the comparison valid while avoiding the cost of maintaining two separate clusters.

---

## 5. Asya-Specific Services (SQS, S3, Gateway, KEDA)

At low load:

- **S3** (results bucket, e.g. `asya-results`):
  - Store at most a few MB of JSON logs → **cents** per month.
- **SQS** (transport queues):
  - First 1M requests/month are often free; even beyond that, cost is very low.
- **CloudWatch Logs**:
  - Basic logs for operator, gateway, handlers → measured in MB/low GB → **cents**.
- **KEDA operator**:
  - Runs inside the same nodes as other pods; no separate cost beyond EC2/EKS.

These do not materially change the cost estimates above for typical dev/test usage.

---

## 6. Recommended Strategy for This Example

1. **Start CPU-only**:
   - Create a small EKS cluster with `t3.large` nodes.
   - Temporarily relax GPU requirements in the `agentic_customer_support` AsyncActors (e.g., remove `nvidia.com/gpu` requests from `response-generator`) to validate the Asya pipeline end-to-end.
   - Deploy both Asya and Ray Serve onto this cluster and run low-load comparisons.
2. **Add GPU nodegroup later (optional)**:
   - Once the plumbing works (operator, KEDA, crew, gateway, actors, Ray app), add a GPU nodegroup and reintroduce GPU requests for the heavy LLM stage in both frameworks.
   - Keep experiments within controlled time windows (2–4 hours), then delete the cluster.
3. **Use AWS Budgets**:
   - Maintain a low monthly **cost budget** (e.g., \$10–\$20) with email alerts.
   - Optionally keep a **zero-spend budget** to notify you as soon as any non-zero spend appears in a new month.

This approach lets you run the agentic customer support example on EKS, compare Asya vs Ray, and stay comfortably within a small monthly budget as long as you tear down clusters when you are done.
