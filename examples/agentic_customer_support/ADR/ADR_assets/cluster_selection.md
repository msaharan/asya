# Cluster selection search results

## 1.
You can obtain a Kubernetes (k8s) cluster with GPUs suitable for two people from several options:

1. Managed GPU Kubernetes clusters on cloud providers like Google Kubernetes Engine (GKE), AWS EKS, and Azure AKS offer GPU node pools. They allow multi-tenant setups with node pools having GPUs such as Nvidia A100 or L4. GKE supports GPU partitioning for sharing GPUs among pods/tenants. These options provide quick deployment, billing by usage, and ease of management.

2. Specialized providers like RunPod offer instant multi-node GPU clusters optimized for AI/ML workloads, deployable on demand and billed by the millisecond, which can be shared between users.

3. Open-source tools like vCluster enable creating multiple isolated virtual Kubernetes clusters on shared GPU infrastructure, enabling multi-tenancy for GPU workloads with full Kubernetes control planes per user.

4. For ultimate control and lower cost over time, you could run your own bare-metal GPU Kubernetes cluster with appropriate multi-tenancy and GPU sharing configured, but this requires hardware and setup efforts.

Examples:
- Google Cloud GKE with GPU node pools and multi-instance GPU partitions can be configured to share GPUs efficiently.
- RunPod instant clusters for GPU workloads deployed instantly.
- Open-source vCluster for creating isolated virtual K8s clusters on shared GPU cloud infrastructure.

This makes cloud-based managed Kubernetes GPU clusters or RunPod's service the best immediate option for two users needing GPU access with isolated Kubernetes environments and pay-per-use pricing. For customized multi-tenant GPU sharing, vCluster is an emerging solution.[1][2][3][4][5][6]

[1](https://www.reddit.com/r/kubernetes/comments/1lofjxh/multitenant_gpu_clusters_with_vcluster_oss_heres/)
[2](https://www.vcluster.com/blog/bare-metal-kubernetes-with-gpu-challenges-and-multi-tenancy-solutions)
[3](https://www.runpod.io/product/instant-clusters)
[4](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gpus-multi)
[5](https://www.vcluster.com/solutions/gpu-cloud-providers)
[6](https://maddevs.io/writeups/how-to-run-pods-within-one-gpu-in-a-gke-cluster/)
[7](https://dev.to/thenjdevopsguy/sharing-a-nvidia-gpu-between-pods-in-kubernetes-4hp9)
[8](https://www.reddit.com/r/kubernetes/comments/1l9l8gz/multitenant_gpu_workloads_are_finally_possible/)
[9](https://www.qumulus.io/kubernetes-vs-vm-cloud-pricing-the-real-cost-breakdown/)
[10](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)

## 2.

To quickly get the hackathon for Asya vs Ray Serve running, here are the key steps and resources:

1. GPU Kubernetes Cluster Access:
- You can get instant GPU clusters with Kubernetes support from cloud providers like Together.ai or Runpod.io that offer multi-GPU clusters ready in minutes.
- Alternatively, set up your own Kubernetes cluster with GPU support on local or cloud infrastructure using guides like installing NVIDIA drivers and configuring Kubernetes device plugins. MicroK8s with GPU sharing is a lightweight option.
- This gives you a scalable, multi-node environment with GPUs needed for running both Asya and Ray Serve workloads.

Useful resources:
- Kubernetes GPU installation and configuration guide: dev.to article (Oct 2024)
- Instant GPU clusters with Kubernetes: together.ai and runpod.io
- Ray Serve features and use cases: an insightful list of pros/cons and capabilities
- MicroK8s GPU share setup walkthrough for lightweight local clusters

Starting with instant GPU clusters or a easy-to-configure MicroK8s cluster will minimize delay. Then choose your use-case and code the basics on Asya and Ray Serve. This will let you quickly build a side-by-side evaluation to deepen documentation and produce content for your YouTube channel or Medium article.

If you want, help can also be coordinated to find specific GPU cluster resources and finalize the use-case design for the hackathon-style evaluation.[1][2][3][4][5][6]

[1](https://dev.to/thenjdevopsguy/gpus-in-kubernetes-installation-and-configuration-51ea)
[2](https://www.runpod.io/articles/guides/deploying-your-ai-hackathon-project-in-a-weekend-with-runpod)
[3](https://www.together.ai/blog/instant-gpu-clusters)
[4](https://deep-dive-devops.com/kubernetes-gpu-share-in-microk8s-step-by-step-guide-2/)
[5](https://www.devopsschool.com/blog/top-10-ai-model-serving-frameworks-tools-in-2025-features-pros-cons-comparison/)
[6](https://www.anyscale.com/blog/deepseek-vllm-ray-google-kubernetes)
[7](https://www.youtube.com/watch?v=eBbjSfxwL30)
[8](https://opensource.org/blog/open-source-ai-and-policy-from-the-perspective-of-east-asia)
[9](https://www.reddit.com/r/kubernetes/comments/1bkmqoo/simple_explainer_on_how_gpu_allocation_to_k8s/)
[10](https://assets.ctfassets.net/xjan103pcp94/7Le2RvgnMgydY1RaD81jGM/d9cc4de603ebf46cfb5d34a06ad40e56/Ray_Open_Source-vs-Anyscale_Platform-Comparison.pdf)

## 3.
Q. Can I run two services one developed on asya and one developed on ray serve on runpod to compare them. And can two users access them at the same time?

You can run two distinct services developed on Asya and Ray Serve on RunPod by deploying each service on separate pods or GPU instances. RunPod supports launching multiple pods concurrently, so each service can run independently in its own environment. This allows you to compare their performance or behavior.

Regarding access by two users simultaneously:
- If you deploy each service on its own pod and expose the required ports, both users can access the services concurrently via their respective URLs.
- RunPod also supports concurrency within services (for serverless functions), letting multiple requests be handled at once.
- For Ray Serve specifically, multi-application deployments are supported by running separate Ray Serve apps with different names and route prefixes, enabling multiple services on the same Ray cluster if desired.

In summary:
- Deploy the Asya service on one RunPod pod.
- Deploy the Ray Serve service on another pod (or both on a single pod if sufficient resources and configuration are set).
- Each service can handle multiple users concurrently as long as the infrastructure and software concurrency settings allow it.

This approach allows you to run and compare both Asya- and Ray-based services on RunPod simultaneously, with concurrent access by multiple users.[1][2][3][4]

[1](https://docs.runpod.io/serverless/development/concurrency)
[2](https://docs.runpod.io/pods/manage-pods)
[3](https://docs.anyscale.com/services/multi-app)
[4](https://github.com/ray-project/ray/issues/31072)
[5](https://www.runpod.io/product/instant-clusters)
[6](https://www.runpod.io/articles/guides/ai-on-a-schedule)
[7](https://www.runpod.io/blog/how-to-run-serverless-ai-and-ml-workloads-on-runpod)
[8](https://www.reddit.com/r/cloudcomputing/comments/1k9rkdx/runpod_how_to_use_the_same_project_files_and/)
[9](https://www.runpod.io/blog/deploy-multimodal-models-runpod)
[10](https://www.runpod.io/blog/instant-clusters-runpod)

## Decision
- RunPod
    - start with RunPod because it's advertised for hackathon projects in [this](https://www.runpod.io/articles/guides/deploying-your-ai-hackathon-project-in-a-weekend-with-runpod) article
    - change later if needed

## Decision
- Can't use RunPod because it doesn't support kubernetes.
-   RunPod website: Do you support Kubernetes or other container orchestration tools?
        - Currently, Instant Clusters are not compatible with Kubernetes. The cluster environment is managed by Runpod's native orchestration system, eliminating the need for additional container orchestration tools or CNI configuration.  
- Next choice: Together.ai or others

### Together.ai pricing

- **Reserved cluster: Reserve GPU capacity for a duration between 1-90 days. The following costs are for 1 day.

| GPU Type            | Bandwidth           | Details                 | Availability | Price                  |
| ------------------- | ------------------- | ----------------------- | ------------ | ---------------------- |
| 8x H100 (80GB SXM)  | 3.2 Tb/s Infiniband | 1 node \| 208 CPU cores | Available    | $480.00 \| $2.50 / Hour |
| 16x H100 (80GB SXM) | 3.2 Tb/s Infiniband | 2 nodes \| 416 CPU cores | Available    | $960.00 \| $2.50 / Hour |

- On demand cluster: Pay for GPU usage by the hour.

| GPU Type            | Bandwidth           | Details                 | Availability | Price                                |
| ------------------- | ------------------- | ----------------------- | ------------ | ------------------------------------ |
| 8x H100 (80GB SXM)  | 3.2 Tb/s Infiniband | 1 node \| 208 CPU cores | Available    | $23.92 / Hour \| $2.99 / Hour per GPU |
| 16x H100 (80GB SXM) | 3.2 Tb/s Infiniband | 2 nodes \| 416 CPU cores | Available    | $47.84 / Hour \| $2.99 / Hour per GPU |

### AWS EKS

- Exploring using AWS EKS for the cluster because [Asya repo](https://github.com/deliveryhero/asya/blob/main/docs/install/aws-eks.md) has a guide for it.
- See [./cost_estimate.md](./cost_estimate.md) for the cost estimate for AWS EKS.

Cluster Prep

  - Make sure your workstation has AWS CLI, kubectl ≥1.24, Helm 3, and (optionally) eksctl, then stand up or reuse an EKS 1.24+ cluster with the usual multi-AZ VPC, NAT gateway, and pod-friendly security groups (docs/install/aws-eks.md:5-24).
  - Create three IAM roles with EKS Pod Identity: asya-operator-role (SQS queue management), asya-actor-role (SQS + S3 access for handlers), and keda-operator-role (read-only SQS) per the JSON snippets in docs/install/aws-eks.md:25-84. You’ll attach them later through service-account annotations.
  - Install core addons: Pod Identity Agent and the latest VPC CNI (docs/install/aws-eks.md:86-96), then deploy KEDA in its own namespace and bind it to keda-operator-role via aws eks create-pod-identity-association (docs/install/aws-eks.md:98-121).
  - Provision an S3 bucket (e.g., asya-results) for final transcripts and escalations (docs/install/aws-eks.md:123-127). The bucket ARN must match the policy attached to asya-actor-role.
  - Because response-generator requests nvidia.com/gpu: 1 (examples/agentic_customer_support/asya_app/config/example-asyncactor.yaml:95-125), add a GPU node group (g4dn or similar) and the NVIDIA device plugin so the pods can schedule onto GPU nodes (docs/install/aws-eks.md:131-150). Cluster Autoscaler and Metrics Server are recommended for hands-off scaling/visibility (docs/install/aws-eks.md:151-170).

    Install the Asya Stack on EKS
    - Apply the CRDs from src/asya-operator/config/crd/ so AsyncActor manifests are recognized (docs/install/aws-eks.md:189-193).
    - Start from the sample operator-values.yaml in docs/install/aws-eks.md:195-210, set your SQS region, and add the IRSA annotation for asya-operator-role. Include any secrets the operator needs for transports (e.g., awsAccessKeyIdSecretRef if not using Pod Identity).
    - Deploy the operator via helm install asya-operator deploy/helm-charts/asya-operator/ -n asya-system --create-namespace -f operator-values.yaml (docs/install/aws-eks md:212-218).
    - If you want to drive the example through HTTP, install the gateway with gateway-values.yaml that points at your SQS region, result bucket, and database plus the asya-gateway-role annotation (docs/install/aws-eks.md:220-248).
    - Deploy the crew chart so happy-end and error-end actors handle terminal routing and S3 persistence (docs/install/aws-eks.md:250-288).
    - Keep the sample AsyncActor spec from docs/install/aws-eks.md:292-316 handy—you’ll mimic its eks.amazonaws.com/role-arn annotation per actor so the sidecar pods can assume asya-actor-role.

  Prepare the Agentic Customer Support Artifacts

  - Export the convenience environment variables from the runbook (examples/agentic_customer_support/docs/runbook-asya.md:17-24): REGISTRY, TAG, NAMESPACE, and ASYA_GATEWAY_URL. For EKS, point REGISTRY at your ECR repo, e.g. ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/customer-support.
  - Build all handler images with REGISTRY=$REGISTRY TAG=$TAG ./scripts/build_asya_images.sh (examples/agentic_customer_support/docs/runbook-asya.md:28-40, examples/agentic_customer_support/scripts/build_asya_images.sh:1-42). The script iterates over all seven handlers and injects the right HANDLER argument into the shared Dockerfile. Push each resulting tag to ECR so the cluster can pull them (examples/agentic_customer_support/docs/runbook-asya.md:36-41).
  - Update examples/agentic_customer_support/asya_app/config/example-asyncactor.yaml so every image: line references the pushed registry/tag (examples/agentic_customer_support/asya_app/config/example-asyncactor.yaml:18-188). While editing, add metadata.annotations.eks.amazonaws.com/role-arn: arn:aws:iam::<account>:role/asya-actor-role to each AsyncActor so the runtime pods inherit the correct permissions, and keep GPU resource requests on response-generator.
  - Ensure examples/agentic_customer_support/asya_app/config/namespace.yaml has the namespace you plan to use (defaults to asya-cs; change it if needed) (examples/agentic_customer_support/asya_app/config/namespace.yaml:1-4).

  Deploy the Example onto EKS

  - From examples/agentic_customer_support, run NAMESPACE=$NAMESPACE ./scripts/deploy_asya.sh to create/update the namespace and apply all AsyncActor CRDs in one shot (examples/
  - If you prefer manual control (or until the script is updated to use asya_app), run kubectl apply -f asya_app/config/namespace.yaml (after substituting the namespace) and
    kubectl apply -n $NAMESPACE -f asya_app/config/example-asyncactor.yaml yourself.
  - Confirm scale-out by watching kubectl get pods -n $NAMESPACE -w and verifying KEDA created the ScaledObjects. Use kubectl describe asyncactor <name> -n $NAMESPACE if anythingfails admission.
  - Use the verification checklist in docs/install/aws-eks.md:322-337 to ensure the operator, KEDA, and AsyncActors are healthy and that aws sqs list-queues shows asya-<actor>entries.

  Validate the Pipeline

  - Once all pods are Ready, run the bundled smoke test: python scripts/send_test_ticket.py --framework asya --ticket examples/test_ticket.json --endpoint
    "$ASYA_GATEWAY_URL" (examples/agentic_customer_support/docs/runbook-asya.md:68-78, examples/agentic_customer_support/scripts/send_test_ticket.py:1-73).
  - Inspect per-actor logs with kubectl logs deployment/<actor> -n $NAMESPACE to confirm each stage processed the envelope (examples/agentic_customer_support/docs/runbook-
    asya.md:85-91). Expect status: completed, a formatted response, and a judge_score ≥0.7; otherwise, the response-validator will route to refinement per the runbook checklist(examples/agentic_customer_support/docs/runbook-asya.md:80-103).
  - Keep the troubleshooting table in mind for CrashLoopBackOff, queue, or gateway issues—most stem from mismatched image tags or missing transport credentials (examples/
    agentic_customer_support/docs/runbook-asya.md:95-104).

  Next steps: (1) enable Cluster Autoscaler/monitoring if you haven’t yet so GPU nodes downscale when idle; (2) capture performance metrics and update the comparison/case-study docs once the example is serving real tickets.
