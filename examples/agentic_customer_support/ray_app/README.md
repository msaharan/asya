# Ray Serve Implementation

This directory contains the Ray Serve-based implementation of the agentic customer support system.

## Architecture

The system uses Ray Serve with a deployment graph that orchestrates the pipeline:

1. **Ticket Ingestion**: HTTP endpoint receives tickets
2. **Intent Classification**: Classifies ticket intent and urgency
3. **Knowledge Retrieval**: Retrieves relevant information from knowledge base
4. **Response Generation**: Generates response using LLM
5. **Response Validation**: Validates response quality using LLM judge
6. **Response Formatting**: Formats and finalizes response
7. **Escalation Handling**: Routes to human agent if needed

## Structure

```
ray_app/
├── serve/            # Ray Serve deployment code
├── handlers/         # Handler classes for each stage
├── config/           # Kubernetes deployment configs
├── tests/            # Unit and integration tests
└── README.md         # This file
```

## Deployment

See `config/` directory for Kubernetes deployment manifests.
