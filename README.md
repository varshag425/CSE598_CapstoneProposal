# Project Schedule Risk Teammate

A minimal deterministic baseline for the CSE 598 Agentic AI capstone proposal.

## Problem

Project schedule risks can emerge through team updates, task delays, and dependencies between project activities. A project manager may need to determine which task is affected, whether the delay threatens downstream work, and whether the issue should be escalated.

The eventual project will develop an AI teammate that can monitor project context, identify schedule risks, investigate their downstream impact, and recommend actions for human review.

The baseline is intentionally smaller. It demonstrates the core workflow using structured project information and a team update.

## Baseline

The baseline is a deterministic Python workflow that:

1. Reads a project schedule and the latest team update.
2. Identifies the affected task from the team update.
3. Traverses the project dependency graph to identify downstream tasks.
4. Compares the observed delay with the available project buffer.
5. Assigns a risk level and escalation decision.
6. Produces an explanation and recommended action.

The baseline uses the following decision policy:

* `delay <= project buffer` → **LOW risk / MONITOR**
* `delay > project buffer` with no downstream dependencies → **MEDIUM risk / ESCALATE**
* `delay > project buffer` with downstream dependencies → **HIGH risk / ESCALATE**

The baseline is intentionally simple so that it establishes a reproducible point of comparison for the future agentic system.

## Requirements

* Python 3.9+
* No external Python packages
* No API key or external service

## Run

From the repository root:

```bash
python run_baseline.py --input examples/test_case.json
```

## Input

The example input is located at:

```text
examples/test_case.json
```

It contains:

* `latest_team_update` — the most recent project or standup update
* `tasks` — the project schedule and dependency information
* `name` — task name
* `delay_days` — observed delay for the task
* `project_buffer_days` — available schedule buffer
* `dependencies` — tasks that must be completed before the current task

For example, the team update may state that:

```text
Electrical Inspection is delayed by four days because the required permit has not been approved.
```

The baseline then identifies `Electrical Inspection` from the update and uses the dependency graph to determine its downstream impact.

## Expected Output for the Included Test Case

```text
Project Schedule Risk Teammate
==============================
Affected Task: Electrical Inspection
Risk Level: HIGH
Decision: ESCALATE
Downstream Impacts: Final Inspection, Project Handover

Reason: Electrical Inspection was identified from the latest team update.
The reported delay is 4 days compared with 2 days of available project buffer.
The delay may affect downstream tasks: Final Inspection, Project Handover.

Recommended Action: Review the blocker, assess downstream schedule impacts,
and evaluate mitigation options.
```

The expected behavior is that the four-day delay exceeds the two-day buffer and the affected task has downstream dependencies. Therefore, the baseline should identify the disruption as **HIGH risk** and recommend **ESCALATE**.

## Reproducibility

No API key, model download, database, external service, or third-party Python package is required.

The baseline can be run with a standard Python 3.9+ installation using the command provided above.

The same input produces the same output because the baseline uses deterministic rules.

## Repository Structure

```text
.
├── run_baseline.py
├── examples/
│   └── test_case.json
├── README.md
└── AI_USAGE.md
```

## Limitations

The baseline does not:

* use an LLM;
* interpret complex or ambiguous project communications;
* retrieve information from Slack or other external project systems;
* maintain persistent project memory;
* calculate a full critical path;
* model schedule uncertainty;
* retrieve historical project information;
* automatically modify the project schedule; or
* make autonomous project decisions.

The baseline only demonstrates a small deterministic workflow for identifying a schedule disruption and assessing its downstream impact.

## Future Agentic System

The semester project will extend the baseline into an AI project teammate.

Potential capabilities include:

* interpreting less-structured team and standup updates;
* identifying affected tasks and project risks;
* inspecting dependency and schedule information through tools;
* retrieving relevant project context and historical information;
* maintaining project state and longer-term context;
* reasoning about downstream consequences;
* participating in requirements and design discussions;
* preparing daily risk summaries;
* recommending mitigation or escalation actions; and
* communicating findings to the project team.

The agent will remain human-in-the-loop. It will recommend actions and surface risks, but a human project manager will approve interventions before they are acted upon.

The baseline therefore provides a simple, reproducible reference point for evaluating whether these additional agentic capabilities improve schedule-risk identification and decision support.
