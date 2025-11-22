# Asya Implementation

This directory contains the Asya-based implementation of the agentic customer support system.

## Architecture

The system uses Asya's actor framework with the following actors:

1. **ticket-ingester**: Receives and validates incoming tickets
2. **intent-classifier**: Classifies ticket intent and urgency
3. **knowledge-retriever**: Retrieves relevant information from knowledge base
4. **response-generator**: Generates response using LLM
5. **response-validator**: Validates response quality using LLM judge
6. **response-formatter**: Formats and finalizes response
7. **escalation-handler**: Handles escalation to human agents

## Structure

```
asya/
├── handlers/          # Python handler functions for each actor
├── config/           # Kubernetes CRDs and configurations
├── tests/            # Unit and integration tests
└── README.md         # This file
```

## Deployment

See `config/` directory for Kubernetes AsyncActor CRDs.
