# Technical Program Management Portfolio

Practical, small-scale demonstrations of enterprise integration and technical delivery practices. These examples use **synthetic data only** and are not extracts from private KMOV systems or customer environments.

## Projects

### 1. [CRM Synchronization Demo](crm-integration-demo/)
A dependency-free Python example demonstrating webhook-like CRM ingestion, deduplication, idempotent updates, conflict handling and audit-friendly output.

### 2. [Technical Program Health Dashboard](tpm-program-dashboard/)
A Python command-line report for tracking project milestones, cross-team dependencies, delivery risks and overdue work. Uses JSON sample data and generates a readable Markdown status report.

## How to run

Requires Python 3.10+; no external services, API keys or paid libraries.

```bash
python crm-integration-demo/crm_sync.py
python tpm-program-dashboard/program_dashboard.py
python -m unittest discover -s tests -v
```

## What this demonstrates

- Systems thinking: contracts, integration boundaries, idempotency and auditability
- Technical delivery: milestones, risks, dependencies and stakeholder reporting
- Operational quality: unit tests, deterministic sample data and GitHub Actions CI

## Scope and provenance

Created as **portfolio demonstrations (October 2026)** to explain technical concepts and program-management decisions. They are not claims of production software ownership or deployments. All organization names, contacts and records in examples are fictional. Technical concepts are informed by enterprise integration, CRM automation and cross-functional delivery experience. Code and documentation were created with AI assistance and are provided for review and learning.

## Security

No real customer records, passwords, private API endpoints, credentials or data from private repositories are included.

MIT License.
