# Agentic Customer Support System

A comparative implementation of an agentic customer support system using both [Asya🎭](https://github.com/deliveryhero/asya) and [Ray Serve](https://docs.ray.io/en/latest/serve/index.html).

## Overview

This project implements a multi-stage agentic customer support pipeline. For detailed use case requirements, pipeline flow, and comparison criteria, see [ADR/ADR_assets/use_case.md](ADR/ADR_assets/use_case.md).

## Project Structure

```
examples/agentic_customer_support/
├── asya/              # Asya implementation
│   ├── handlers/      # Python handler functions
│   ├── config/        # Kubernetes CRDs and namespace
│   ├── tests/         # Unit tests
│   ├── Dockerfile     # Container image definition
│   ├── requirements.txt
│   └── README.md
├── ray_app/           # Ray Serve implementation
│   ├── handlers/      # Handler classes
│   ├── serve/         # Ray Serve deployment code
│   ├── config/        # Kubernetes deployments and namespace
│   ├── tests/         # Unit tests
│   ├── Dockerfile     # Container image definition
│   ├── requirements.txt
│   └── README.md
├── scripts/           # Deployment and testing scripts
│   ├── build_asya_images.sh
│   ├── build_ray_image.sh
│   ├── deploy_asya.sh
│   ├── deploy_ray.sh
│   └── send_test_ticket.py
├── docs/              # Documentation hub and guides
│   ├── README.md
│   ├── getting-started.md
│   ├── runbook-asya.md
│   ├── runbook-ray.md
│   ├── comparison.md
│   └── case-study.md
├── examples/          # Test data and examples
│   ├── test_ticket.json
│   └── README.md
├── ADR/               # Architectural Decision Records
│   ├── ADR.md
│   └── ADR_assets/
│       ├── cluster_selection.md
│       └── use_case.md
├── TODO.md            # Project TODO list
├── requirements.txt   # Common dependencies
└── README.md          # This file
```

## Quick Start

For detailed setup and deployment instructions, start with the [documentation hub](docs/README.md) or go straight to the [Getting Started guide](docs/getting-started.md).

**Prerequisites:**
- Kubernetes cluster with GPUs enabled (see [ADR/ADR.md](ADR/ADR.md))
- Python 3.10+, Docker, kubectl

**Quick Overview:**
- **Asya**: Deploy AsyncActor CRDs with handler functions
- **Ray Serve**: Deploy Ray Serve application with deployment graph

Both implementations include unit tests, Dockerfiles, and Kubernetes configurations ready for deployment.

## Comparison

See [Comparison](docs/comparison.md) for detailed breakdown of:
- Development experience
- Deployment & operations
- Performance metrics
- Reliability
- Cost analysis

## Project Status

See [TODO.md](TODO.md) for the complete project checklist and progress tracking.

## Resources

- [Asya Documentation](https://github.com/deliveryhero/asya)
- [Ray Serve Documentation](https://docs.ray.io/en/latest/serve/index.html)
- [Use Case Details](ADR/ADR_assets/use_case.md)
- [Documentation Hub](docs/README.md)
- [Getting Started Guide](docs/getting-started.md)
- [Asya Deployment Runbook](docs/runbook-asya.md)
- [Ray Serve Deployment Runbook](docs/runbook-ray.md)
