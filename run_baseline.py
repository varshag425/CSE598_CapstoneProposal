import argparse
import json


def identify_affected_task(team_update, tasks):
    """Identify the task associated with the latest team update."""
    update_text = team_update.lower()

    for task in tasks:
        task_name = task["name"].lower()
        if task_name in update_text:
            return task

    return None


def find_downstream_tasks(task_name, tasks):
    """Find tasks that directly or indirectly depend on the affected task."""
    downstream = []
    queue = [task_name]
    visited = set()

    while queue:
        current = queue.pop(0)

        if current in visited:
            continue

        visited.add(current)

        for task in tasks:
            if current in task.get("dependencies", []):
                downstream.append(task["name"])
                queue.append(task["name"])

    return downstream


def assess_schedule_risk(affected_task, downstream_tasks):
    delay = affected_task["delay_days"]
    buffer = affected_task["project_buffer_days"]

    if delay <= buffer:
        risk = "LOW"
        decision = "MONITOR"
        action = (
            "Continue monitoring the task and review the blocker "
            "during the next project update."
        )
    elif downstream_tasks:
        risk = "HIGH"
        decision = "ESCALATE"
        action = (
            "Review the blocker, assess downstream schedule impacts, "
            "and evaluate mitigation options."
        )
    else:
        risk = "MEDIUM"
        decision = "ESCALATE"
        action = (
            "Investigate the blocker and evaluate schedule mitigation "
            "options."
        )

    return risk, decision, action


def analyze_project(project):
    tasks = project["tasks"]
    team_update = project["latest_team_update"]

    # Step 1: identify affected task from team context
    affected_task = identify_affected_task(team_update, tasks)

    if affected_task is None:
        return {
            "affected_task": "UNKNOWN",
            "risk_level": "UNKNOWN",
            "decision": "REVIEW",
            "downstream_impacts": [],
            "reason": (
                "The team update could not be confidently associated "
                "with a task in the project schedule."
            ),
            "recommended_action": (
                "Request clarification from the project team."
            ),
        }

    # Step 2: inspect dependency graph
    downstream_tasks = find_downstream_tasks(
        affected_task["name"],
        tasks
    )

    # Step 3: assess schedule risk
    risk, decision, action = assess_schedule_risk(
        affected_task,
        downstream_tasks
    )

    # Step 4: generate explanation
    delay = affected_task["delay_days"]
    buffer = affected_task["project_buffer_days"]

    if downstream_tasks:
        impact_text = (
            "The delay may affect downstream tasks: "
            + ", ".join(downstream_tasks)
            + "."
        )
    else:
        impact_text = "No downstream dependent tasks were identified."

    reason = (
        f"{affected_task['name']} was identified from the latest "
        f"team update. The reported delay is {delay} days compared "
        f"with {buffer} days of available project buffer. "
        f"{impact_text}"
    )

    return {
        "affected_task": affected_task["name"],
        "risk_level": risk,
        "decision": decision,
        "downstream_impacts": downstream_tasks,
        "reason": reason,
        "recommended_action": action,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Project Schedule Risk Teammate baseline."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to project context JSON"
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        project = json.load(f)

    result = analyze_project(project)

    print("Project Schedule Risk Teammate")
    print("==============================")
    print(f"Affected Task: {result['affected_task']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Decision: {result['decision']}")
    print(
        "Downstream Impacts: "
        + (
            ", ".join(result["downstream_impacts"])
            if result["downstream_impacts"]
            else "None"
        )
    )
    print()
    print(f"Reason: {result['reason']}")
    print()
    print(
        f"Recommended Action: "
        f"{result['recommended_action']}"
    )


if __name__ == "__main__":
    main()
