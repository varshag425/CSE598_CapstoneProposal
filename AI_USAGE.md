# AI Usage / Trace

AI tools used:
- ChatGPT

Purpose of AI assistance:
- Project ideation and scope refinement
- Operational definition refinement
- Baseline implementation assistance
- README drafting assistance

### Trace

Prompt: (Provided context files from earlier project work along with CSE 598 assignment details) map out Step 2 — Freeze the operational definition
Reply: 
Perfect. Let's freeze the operational definition before touching code. This is the most important step because the proposal rubric explicitly asks for a problem where another person can tell whether the system succeeds or fails.

I also want to make one refinement to our earlier wording: the baseline should make a decision about escalation, not claim to predict project completion risk. That keeps the problem narrow, measurable, and honest.

Step 2 — Freeze the Operational Definition
Working project

Schedule Risk Escalation Agent

1. Target user

Project managers / project controls personnel monitoring project schedules and responding to task delays.

The user isn't asking the system to manage the whole project. They're asking:

“I just learned that this task is delayed. Does this require my attention, and what should I do next?”

That is our core workflow.

2. Exact input

The baseline receives a single structured schedule-update record.

For tonight, let's keep the input deliberately small:

Task name
Original/expected duration
Observed delay
Remaining project buffer
Whether the task has downstream dependent tasks

For example:

{
  "task": "Electrical Inspection",
  "delay_days": 4,
  "project_buffer_days": 2,
  "has_downstream_dependencies": true
}
Why these fields?

They give us enough information to make a defensible decision without pretending we're building a complete project scheduling system.

The critical relationship is:

Observed delay vs. available project buffer

and the downstream-dependency flag provides a simple indication of whether the delay can propagate.

3. Exact decision

The agent makes one primary operational decision:

ESCALATE or MONITOR

ESCALATE if the observed delay exceeds the available project buffer.

MONITOR otherwise.

Then we can refine severity:

Condition	Risk level	Decision
Delay ≤ buffer	LOW	MONITOR
Delay > buffer, no downstream dependencies	MEDIUM	ESCALATE
Delay > buffer + downstream dependencies	HIGH	ESCALATE

This is deliberately deterministic for the baseline.

Why this is important

We're not saying:

“Our algorithm knows this project will be late.”

We're saying:

“Given a predefined operational policy, does this observed delay warrant escalation?”

That's something we can actually evaluate.

4. Exact output

The baseline will return four things:

Risk Level
Decision
Reason
Recommended Action

For example:

Risk Level: HIGH
Decision: ESCALATE

Reason:
The observed delay exceeds the available project buffer and
the affected task has downstream dependencies.

Recommended Action:
Review downstream tasks and evaluate schedule mitigation options.

The decision is the core output.

The reason/action make the output useful to a human stakeholder and give us something richer to improve later.

5. What counts as SUCCESS?

We need to be very explicit here.

For the baseline:

Success

The system succeeds when it:

correctly applies the escalation rule;
assigns the appropriate risk level according to the predefined rules; and
produces the corresponding recommended action.

For example:

delay = 4 days
buffer = 2 days

Since:

4 > 2

the correct decision is:

ESCALATE
6. What counts as FAILURE?

The baseline fails when it:

incorrectly chooses MONITOR when escalation is warranted;
incorrectly chooses ESCALATE when the delay is within the available buffer;
assigns the wrong severity under the defined rules;
or produces an action inconsistent with its decision.

This gives us binary decision accuracy as our simplest evaluation metric.

7. The actual agentic workflow

Here's where I think we should be careful.

Tonight's baseline isn't really a sophisticated agent.

And that's okay.

The baseline is the initial policy for the eventual agent:

                 Schedule Update
                       │
                       ▼
                  PERCEPTION
               Extract schedule
                   information
                       │
                       ▼
                   DECISION
            Does delay exceed buffer?
                       │
              ┌────────┴────────┐
              ▼                 ▼
          MONITOR            ESCALATE
                                │
                                ▼
                             ACTION
                     Recommend investigation/
                     mitigation of downstream
                           schedule impact

That's enough of an agentic framing for the proposal.

Later, an improved system could replace the simple rule with an agent that actually investigates the schedule before deciding.

For example:

Schedule update
      ↓
Observe
      ↓
Inspect dependency graph
      ↓
Check critical-path impact
      ↓
Retrieve historical/project information
      ↓
Reason about risk
      ↓
Choose action
      ↓
Human approval

That distinction is valuable.

We're not claiming that the baseline already performs all of this.

8. What we are explicitly NOT doing tonight

This is just as important.

Out of baseline scope:
Full project scheduling
Automatic CPM calculation
Monte Carlo simulation
Predicting final project completion date
LLM reasoning
RAG
External project-management APIs
Automatic modification of schedules
Multi-agent architecture
Web application
Authentication/database
Real-world project data

Those things can make the future project richer, but none are necessary for the proposal baseline.

The assignment explicitly says the baseline may be a simple rule-based system and emphasizes that it needs to be runnable and reproducible.

9. One thing I'd change from our earlier idea

I originally suggested:

delay > buffer → ESCALATE

That's good for the baseline, but too simplistic as the entire proposed project.

So I would frame the semester-level problem as:

An agent that evaluates whether a schedule disruption warrants escalation by investigating its potential downstream impact and recommending an appropriate intervention.

Then:

Baseline
delay vs. buffer
Proposed agent
delay
 ↓
inspect dependencies
 ↓
assess downstream impact
 ↓
consider project context
 ↓
decide escalation
 ↓
recommend intervention

That creates a very clean baseline → improvement story.

10. The frozen version

Unless you see something you dislike, this is what I'd lock into the proposal:

Problem: Project managers often need to determine whether an observed task delay requires immediate intervention or can be safely monitored. The proposed Schedule Risk Escalation Agent will analyze schedule updates, assess the relationship between observed delays and available schedule buffer, and determine whether the disruption warrants escalation. The system will output a risk level, an escalation decision, an explanation, and a recommended next action.

Input: A structured schedule-update record containing the affected task, observed delay, available project buffer, and downstream dependency information.

Output: Risk level (LOW, MEDIUM, or HIGH), decision (MONITOR or ESCALATE), reason, and recommended action.

Baseline decision policy: A delay within the available project buffer is monitored. A delay exceeding the buffer is escalated, with higher severity assigned when downstream dependencies are present.

Success: The system correctly applies the predefined decision policy and produces the corresponding risk level and action.

Failure: The system incorrectly escalates/does not escalate a disruption or produces an inconsistent risk assessment or recommendation.

I think this is the right level. It is simple enough to build tonight, but the problem itself isn't trivial: it is an operational decision-support problem with a clear path toward an actual agent.

And importantly, it is connected to your prior work without simply submitting your old project with an LLM slapped on it.

One decision before we code

I'd make one small choice now:

Should has_downstream_dependencies be a simple boolean?

Option A — Yes (recommended for tonight)

"has_downstream_dependencies": true

Extremely easy and robust.

Option B — Give us actual dependent task names
"dependent_tasks": [
    "Final Inspection",
    "Project Handover"
]

This is a little more realistic and makes the output more compelling, while still being trivial to implement.

I'd choose Option B. It gives us a better screenshot and sets up a natural future dependency-graph agent without adding much complexity tonight.

If we lock that in, Step 3 is the fun part: we'll write the tiny baseline, run an actual test case, and get the screenshot-ready output.



Prompt: Move onto step 3: Code the baseline
Reply:
Yes. Step 3 is done. I deliberately kept this deterministic and dependency-free. 

I also made one small implementation choice from Step 2: actual downstream task names, rather than just a boolean. It makes the test case/output look more credible while adding essentially no complexity.

What I built

The baseline is:

Schedule update
      ↓
Read delay + buffer + downstream tasks
      ↓
Apply deterministic policy
      ↓
LOW / MEDIUM / HIGH
      ↓
MONITOR / ESCALATE
      ↓
Recommended action

For the concrete test case:

Task: Electrical Inspection
Delay: 4 days
Buffer: 2 days
Downstream tasks:
    Final Inspection
    Project Handover

The verified output is:

Schedule Risk Assessment
========================
Task: Electrical Inspection
Risk Level: HIGH
Decision: ESCALATE

Reason: The observed delay (4 days) exceeds the available project buffer
(2 days) and affects downstream tasks: Final Inspection, Project Handover.

Recommended Action: Review downstream tasks and evaluate schedule
mitigation options.

I actually ran the script successfully, rather than just writing code that should work.

I've packaged the initial repository contents here:

Download the runnable baseline

It contains:

schedule-risk-agent/
├── run_baseline.py
├── README.md
├── AI_USAGE.md
├── requirements.txt
└── examples/
    └── test_case.json

The baseline uses no external packages and no API key, which is excellent for the reproducibility requirement. Your assignment explicitly emphasizes that the TA should be able to reproduce the baseline, and the template asks for dependencies, setup, exact command, input/output locations, and limitations.

One important thing before we move on

I would not submit this exact wording as the final project description yet.

The code is intentionally simple. The proposal needs to make clear that this is the baseline, not the final agent.

The interesting research/engineering question is:

Can an agent improve upon a simple buffer-based escalation policy by inspecting schedule dependencies and project context before deciding whether a disruption warrants intervention?

That's the sentence I want to build the proposal around.

So the progression becomes:

Baseline tonight
delay > buffer?
      ↓
ESCALATE / MONITOR
Proposed agent
Schedule disruption
        ↓
      Observe
        ↓
Inspect affected task/dependencies
        ↓
Assess downstream impact
        ↓
Determine whether intervention is warranted
        ↓
   ESCALATE / MONITOR
        ↓
Recommend next action

That gives you a legitimate reason for an agentic system to exist rather than just wrapping an LLM around a calculator.


Prompt: Let's workshop the capstone proposal document now
Reply: 
# CSE 598 Capstone Project Proposal

## Project Title

**Schedule Risk Escalation Agent**

## 1. Problem Definition

Project schedules frequently change when individual tasks are delayed. A project manager or project controls professional must determine whether a delay can be monitored or whether it requires intervention. This decision can depend not only on the size of the delay, but also on the amount of schedule buffer remaining and whether the delayed task affects downstream work.

This project proposes an agent that evaluates a schedule disruption and determines whether it warrants escalation.

**Target user:** Project managers and project controls personnel.

**Input:** A structured schedule-update record containing:

* the affected task,
* observed delay in days,
* available project buffer in days, and
* downstream dependent tasks.

**Output:**

* risk level: LOW, MEDIUM, or HIGH;
* decision: MONITOR or ESCALATE;
* explanation for the decision; and
* recommended next action.

For the initial baseline, the decision policy is:

* If the delay is less than or equal to the available project buffer, classify the disruption as **LOW** risk and **MONITOR** it.
* If the delay exceeds the available buffer and there are no downstream dependent tasks, classify it as **MEDIUM** risk and **ESCALATE** it.
* If the delay exceeds the available buffer and affects downstream tasks, classify it as **HIGH** risk and **ESCALATE** it.

A successful system must apply this policy consistently and produce the appropriate risk level and action. A failure occurs when the system produces an incorrect escalation decision, risk level, or inconsistent recommended action.

## 2. Motivation and Project Scope

Schedule disruptions are often reviewed manually, even when basic schedule information is already available. A useful AI system could assist with the initial triage of disruptions by determining which changes deserve immediate attention and explaining why.

The project is motivated by my previous work with project schedule risk and simulation-based analysis. Rather than attempting to reproduce a full project scheduling or Monte Carlo system, this project focuses on a narrower operational decision: **whether a schedule disruption should be escalated for intervention**.

The initial baseline intentionally uses a deterministic policy so that its behavior is transparent and reproducible. The longer-term agent could extend this workflow by inspecting a dependency graph, identifying downstream impacts, reasoning about the consequences of a disruption, and recommending possible mitigation actions. These extensions would provide opportunities to explore agentic behaviors such as tool use, planning, and stateful reasoning.

The project will **not** initially attempt to:

* generate complete project schedules;
* calculate or optimize a project's critical path;
* predict an exact project completion date;
* perform Monte Carlo simulation;
* automatically modify a project schedule;
* integrate with external project-management systems; or
* make autonomous decisions without human review.

## 3. Runnable Baseline

The initial baseline is a Python-based rule system that reads a JSON schedule-update record and produces a risk assessment.

The baseline is intentionally simple and does not require an external model, API key, database, or third-party service. Its purpose is to establish a deterministic, runnable reference system against which later agentic approaches can be evaluated.

The baseline implementation is available in the public repository:

[GitHub repository](https://github.com/varshag425/CSE598_CapstoneProposal?utm_source=chatgpt.com)

The repository contains the baseline implementation, test input, README, and AI usage documentation.

## 4. Test Case and Baseline Output

A concrete test case is provided using an **Electrical Inspection** task:

**Input:**

* Task: Electrical Inspection
* Observed delay: 4 days
* Available project buffer: 2 days
* Downstream tasks: Final Inspection, Project Handover

Because the four-day delay exceeds the two-day project buffer and affects downstream tasks, the baseline classifies the disruption as HIGH risk and recommends escalation.

**Actual baseline output:**

```text
Schedule Risk Assessment
========================
Task: Electrical Inspection
Risk Level: HIGH
Decision: ESCALATE

Reason: The observed delay (4 days) exceeds the available
project buffer (2 days) and affects downstream tasks:
Final Inspection, Project Handover.

Recommended Action: Review downstream tasks and evaluate
schedule mitigation options.
```

This output was generated by running the baseline implementation against the test case in the repository.

## 5. Reproducibility and Run Instructions

The baseline requires **Python 3.9 or later** and has no external package dependencies.

After cloning the repository, the baseline can be run with:

```bash
python run_baseline.py --input examples/test_case.json
```

The input format is a JSON object containing the task name, delay, project buffer, and dependent tasks.

The system is deterministic: the same input will produce the same output. No API credentials, external services, model downloads, or databases are required.

The repository README provides the complete setup and execution instructions.

## 6. Initial Evaluation Plan

The initial evaluation will test whether the system correctly applies the predefined escalation policy.

I will construct a small set of schedule-update cases covering the main decision boundaries:

1. Delay within available buffer → LOW / MONITOR.
2. Delay equal to available buffer → LOW / MONITOR.
3. Delay exceeding buffer with no downstream tasks → MEDIUM / ESCALATE.
4. Delay exceeding buffer with downstream tasks → HIGH / ESCALATE.

The primary evaluation metrics will be:

* **decision accuracy**: whether MONITOR vs. ESCALATE is correct;
* **risk-level accuracy**: whether LOW, MEDIUM, or HIGH is correct; and
* **action consistency**: whether the recommended action corresponds to the decision.

For later versions, the baseline can serve as a reference system for evaluating an LLM-based or tool-using agent. Additional evaluation can examine whether the agent correctly identifies relevant downstream impacts, produces useful explanations, and avoids inappropriate escalation.

## 7. Limitations and Next Steps

The current baseline uses a fixed decision policy and therefore does not perform genuine reasoning about complex project schedules. It does not calculate critical paths, model uncertainty, inspect a complete dependency graph, retrieve historical project information, or consider factors such as task priority and resource constraints.

The main next step is to develop the baseline into an agentic workflow. A future version could use tools to inspect a project dependency graph, identify affected downstream tasks, assess schedule impact, and generate a recommendation for human review. An LLM could be introduced for interpreting less-structured schedule information and explaining the assessment, while deterministic checks could remain responsible for important decision boundaries.

Potential future components include:

* dependency-graph inspection;
* critical-path or schedule-impact analysis;
* tool-based retrieval of project information;
* LLM-based reasoning and explanation;
* historical schedule information through retrieval; and
* human approval before any recommended intervention is acted upon.

The baseline therefore provides a simple and reproducible starting point while leaving room to investigate more capable agentic behavior during subsequent phases of the project.

## AI Usage

AI tools were used during project development for brainstorming possible project directions, refining the problem scope, assisting with the baseline implementation, and drafting documentation. AI usage is documented separately in the repository's `AI_USAGE.md` file.
