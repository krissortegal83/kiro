# Technical Program Health Dashboard

A concise command-line demonstration of how a TPM can surface blockers, risk and milestone progress across backend, frontend, AI/ML, data and QA workstreams. Uses **fictional delivery data**.

## Run

\`\`\`bash
python tpm-program-dashboard/program_dashboard.py
python -m unittest discover -s tests -v
\`\`\`

The script prints a Markdown status report suitable for pasting into a project review or team update.

## Features

- Cross-workstream milestone reporting and completion counts
- Deadline flags and dependency-based blockers
- Risk escalation for high risk scores
- Missing/circular dependency checks (prevents misleading program reports)
- Action prompts for the TPM to follow up with owners

## Model and limitations

- \`risk_score\` is a simplified 0–5 demonstration value, not a calibrated prediction.
- The sample date is fixed so the example remains reproducible.
- Real TPM programs require owners, RACI, budget, capacity, release gates, and stakeholder-approved definitions of delivery health.
- Does not communicate with any production project tracker or AI vendor.

## Workflow

\`\`\`text
Milestone JSON -> Dependency validation -> Status / risks -> Markdown report
\`\`\`

This portfolio exercise demonstrates planning and communication, not a claimed production deployment.
