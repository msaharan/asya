# Getting Started Guide

This guide will help you set up and run both implementations of the agentic customer support system.

> Part of the [documentation hub](./README.md). Refer back there anytime you need the full map.

## Prerequisites

1. **Kubernetes Cluster**: You'll need a Kubernetes cluster with:
   - GPU support (for LLM inference)
   - Access to install operators (Asya and/or Ray)
   - kubectl configured

2. **Local Development Environment**:
   - Python 3.10+
   - Docker
   - Make (optional, for convenience)

3. **Queue/Transport** (for Asya):
   - AWS SQS (recommended for cloud)
   - RabbitMQ (for self-hosted)

## Setup Steps

### 1. Clone and Install Dependencies

> Run the following commands from the root of the Asya repo unless noted.

```bash
cd examples/agentic_customer_support

# Install common dependencies
pip install -r requirements.txt

# Install Asya dependencies (if testing Asya)
cd asya
pip install -r requirements.txt

# Install Ray Serve dependencies (if testing Ray)
cd ../ray_app
pip install -r requirements.txt

# Return to the Asya repo root for the following steps
cd ../..
```

### 2. Local Testing

#### Test Asya Handlers Locally

```bash
cd asya

# Run unit tests
pytest tests/

# Test individual handler
python -c "
from handlers.ticket_ingester import process
ticket = {
    'ticket_id': 'TEST-001',
    'customer_id': 'CUST-123',
    'message': 'I need help with my order'
}
result = process(ticket)
print(result)
"
```

#### Test Ray Serve Locally

```bash
cd examples/agentic_customer_support

# Install Ray Serve (if not already installed)
pip install "ray[serve]>=2.9.0"

# Start Ray Serve locally (ensure the example root is on PYTHONPATH)
PYTHONPATH=$(pwd) ray serve run ray_app.serve.pipeline:build_app

# In another terminal, test the endpoint
curl -X POST http://localhost:8000/support \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TEST-001",
    "customer_id": "CUST-123",
    "message": "I need a refund for my order"
  }'

# Stop Ray Serve
ray stop
```

### 3. Build Docker Images

#### Asya Handlers

```bash
cd asya

# Build individual handler images
docker build -t customer-support/ticket-ingester:latest \
  --build-arg HANDLER=handlers.ticket_ingester.process \
  -f Dockerfile .

docker build -t customer-support/intent-classifier:latest \
  --build-arg HANDLER=handlers.intent_classifier.IntentClassifier.process \
  -f Dockerfile .

# ... repeat for other handlers
```

#### Ray Serve

```bash
cd ray_app

docker build -t customer-support/ray-serve:latest -f Dockerfile .
```

### 4. Deploy to Kubernetes

#### Asya Deployment

1. **Install Asya Operator**:
   ```bash
   # Follow Asya installation guide
   # https://github.com/deliveryhero/asya
   ```

2. **Configure Transport** (SQS or RabbitMQ):
   - For SQS: Configure AWS credentials
   - For RabbitMQ: Deploy RabbitMQ operator

3. **Deploy AsyncActors**:
   ```bash
   kubectl apply -f asya/config/example-asyncactor.yaml
   ```

4. **Verify Deployment**:
   ```bash
   kubectl get asyncactors
   kubectl get pods -l app=asya
   ```

#### Ray Serve Deployment

1. **Install Ray Operator**:
   ```bash
   # Follow Ray Kubernetes operator guide
   # https://docs.ray.io/en/latest/cluster/kubernetes/index.html
   ```

2. **Deploy Ray Serve**:
   ```bash
   kubectl apply -f ray_app/config/example-deployment.yaml
   ```

3. **Verify Deployment**:
   ```bash
   kubectl get pods -l app=ray-serve-customer-support
   kubectl port-forward svc/ray-serve-customer-support 8000:8000
   ```

### 5. Send Test Tickets

#### Asya

```bash
# If using Asya Gateway/MCP
# Send ticket to gateway endpoint

# Or directly to queue (if using SQS)
aws sqs send-message \
  --queue-url <queue-url> \
  --message-body "$(cat examples/test_ticket.json)"
```

#### Ray Serve

```bash
# Get service endpoint
SERVICE_URL=$(kubectl get svc ray-serve-customer-support -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Send test ticket
curl -X POST http://${SERVICE_URL}:8000/support \
  -H "Content-Type: application/json" \
  -d @examples/test_ticket.json
```
