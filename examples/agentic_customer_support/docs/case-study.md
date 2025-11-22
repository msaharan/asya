# Case Study: Agentic Customer Support System

> **Comparison**: Asya vs Ray Serve  
> **Use Case**: Multi-stage AI pipeline for customer support  
> **Status**: In Progress  
> **Repository**: [`examples/agentic_customer_support`](../README.md)

## Overview

This case study compares Asya and Ray Serve for building an agentic customer support system that processes customer tickets through a multi-stage pipeline including intent classification, knowledge retrieval, LLM response generation, and validation.

> Part of the [documentation hub](./README.md). Update this narrative after each round of testing.

## Use Case

For the complete use case description including pipeline stages, flow diagram, key requirements, and comparison criteria, see [ADR/ADR_assets/use_case.md](../ADR/ADR_assets/use_case.md).

**Summary**: The system processes customer support tickets through a multi-stage pipeline (ingestion → classification → retrieval → generation → validation → formatting → escalation) with requirements for scalability, cost efficiency, near-realtime latency, and reliability.

## Implementation Comparison

### Asya Implementation

**Code Style**: Pure Python functions/classes - no infrastructure code

```python
# handlers/intent_classifier.py
class IntentClassifier:
    def __init__(self, model_path: str = None):
        self.model_path = model_path

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Pure Python - no decorators, no infrastructure
        intent = self._classify_intent(payload['message'])
        payload['intent'] = intent
        return payload
```

**Deployment**: Kubernetes CRDs handle all infrastructure

```yaml
apiVersion: asya.sh/v1alpha1
kind: AsyncActor
metadata:
  name: intent-classifier
spec:
  transport: sqs
  scaling:
    enabled: true
    minReplicas: 0
    maxReplicas: 20
```

### Ray Serve Implementation

**Code Style**: Ray Serve decorators and deployment graphs

```python
@serve.deployment(
    name="intent-classifier",
    autoscaling_config={...}
)
class IntentClassifierDeployment:
    def __init__(self):
        self.classifier = IntentClassifier()

    async def __call__(self, request):
        return self.classifier.classify(request)
```

**Deployment**: Kubernetes deployments with Ray operator

## Key Findings

> **Note**: Findings will be populated after deployment and performance testing

### Development Experience

- **Asya**: [TBD - to be filled after evaluation]
- **Ray Serve**: [TBD - to be filled after evaluation]

### Performance

| Metric | Asya | Ray Serve |
|--------|------|-----------|
| End-to-end Latency | [TBD] | [TBD] |
| Throughput | [TBD] | [TBD] |
| Resource Efficiency | [TBD] | [TBD] |

### Operational Complexity

- **Asya**: [TBD]
- **Ray Serve**: [TBD]

## Recommendations

[TBD after evaluation]

## Code Repository

Full implementation and comparison available at [`examples/agentic_customer_support`](../README.md).

## Lessons Learned

[TBD - key insights from the comparison]

---

*This case study is part of an ongoing comparison project. Final findings will be updated as testing progresses.*
