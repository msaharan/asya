# Agentic CS Documentation Hub

Central guide to every document in `examples/agentic_customer_support`. Each
section links to the latest source of truth so you don't have to guess
which markdown file to open.

## Quick Map

- **Project Overview**
  - [`../README.md`](../README.md) – high-level project intro
  - [`../ADR/ADR_assets/use_case.md`](../ADR/ADR_assets/use_case.md) – full use case and requirements
- **Setup & Local Dev**
  - [`getting-started.md`](getting-started.md) – cloning, dependencies, local testing, and Kubernetes deployment workflow for both frameworks
- **Deployment Runbooks**
  - [`runbook-asya.md`](runbook-asya.md) – Asya build, deploy, and validation steps
  - [`runbook-ray.md`](runbook-ray.md) – Ray Serve build, deploy, and validation steps
- **Analysis & Reporting**
  - [`comparison.md`](comparison.md) – evaluation matrix (experience, ops, performance, cost)
  - [`case-study.md`](case-study.md) – narrative case study meant for upstream Asya docs
- **Reference Assets**
  - [`../ADR/ADR.md`](../ADR/ADR.md) – architectural decisions
  - [`../ADR/ADR_assets/cluster_selection.md`](../ADR/ADR_assets/cluster_selection.md) – cluster criteria

## How to Use This Hub

1. **New contributor?** Start with the Overview, then follow the Getting Started guide end-to-end.
2. **Deploying Asya or Ray Serve?** Jump directly to the corresponding runbook.
3. **Collecting findings?** Keep `comparison.md` as the canonical checklist and sync highlights into `case-study.md`.
4. **Need architecture context?** Scan the ADRs linked above.

Update this page whenever you add or significantly change a document so the map stays accurate.
