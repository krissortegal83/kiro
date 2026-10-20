# CRM Integration & Idempotent Synchronization Demo

A minimal proof of concept for synchronizing incoming CRM contact events with an existing data set. **Synthetic data only. No credentials or live CRM services.**

## Run

\`\`\`bash
python crm-integration-demo/crm_sync.py
python -m unittest discover -s tests -v
\`\`\`

## Design decisions

- **Identity:** normalize email addresses for case-insensitive deduplication.
- **Idempotency:** replaying an identical event produces an \`unchanged\` action, not a duplicate contact.
- **Conflict resolution:** newer timestamps win; stale data is ignored; conflicting changes with equal timestamps are flagged.
- **Auditability:** every incoming event yields an action in an audit list.
- **Input validation:** reject missing email/name and timestamps without timezone information.
- **Scope:** memory-only example; a production integration would require authentication, API rate-limit handling, durable event IDs, persistence, retry/backoff, monitoring and a conflict review process.

## Architecture

\`\`\`text
Synthetic CRM records -> Validate/normalize -> Merge policy -> Contacts
                                        |             |
                                        +-------------+--> Audit events
\`\`\`

Business context: an illustrative way to discuss reliable CRM integration and delivery risks with engineering teams. Not a production deployment or integration with proprietary systems.
