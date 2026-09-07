# Schedule Risk Escalation Agent

A minimal rule-based baseline for the CSE 598 Agentic AI capstone proposal.

## Problem

Given a project schedule update, determine whether an observed task delay should be monitored or escalated based on the available project buffer and downstream dependencies.

## Baseline

The baseline uses a deterministic decision policy:

- Delay <= project buffer -> LOW risk / MONITOR
- Delay > project buffer with no downstream dependencies -> MEDIUM risk / ESCALATE
- Delay > project buffer with downstream dependencies -> HIGH risk / ESCALATE

The baseline is intentionally simple so that it establishes a reproducible point of comparison for a future agentic system.

## Requirements

- Python 3.9+
- No external Python packages

## Run

From the repository root:

```bash
python run_baseline.py --input examples/test_case.json
```

## Input

The example input is located at:

`examples/test_case.json`

It contains:
- task
- delay_days
- project_buffer_days
- dependent_tasks

## Expected output for the included test case

```text
Schedule Risk Assessment
========================
Task: Electrical Inspection
Risk Level: HIGH
Decision: ESCALATE

Reason: The observed delay (4 days) exceeds the available project buffer (2 days) and affects downstream tasks: Final Inspection, Project Handover.

Recommended Action: Review downstream tasks and evaluate schedule mitigation options.
```

## Reproducibility

No API key, model download, database, or external service is required. The baseline can be run with a standard Python installation.

## Limitations

The baseline does not calculate a project critical path, simulate schedule uncertainty, inspect a complete dependency graph, retrieve historical project information, or use an LLM. It applies only the explicit rules described above.
