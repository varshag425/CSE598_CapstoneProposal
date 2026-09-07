import argparse
import json


def assess_schedule_risk(update):
    delay = update["delay_days"]
    buffer = update["project_buffer_days"]
    dependents = update.get("dependent_tasks", [])

    if delay <= buffer:
        risk = "LOW"
        decision = "MONITOR"
        reason = (
            f"The observed delay ({delay} days) is within the "
            f"available project buffer ({buffer} days)."
        )
        action = "Continue monitoring the task and downstream schedule."
    elif dependents:
        risk = "HIGH"
        decision = "ESCALATE"
        reason = (
            f"The observed delay ({delay} days) exceeds the available "
            f"project buffer ({buffer} days) and affects downstream tasks: "
            f"{', '.join(dependents)}."
        )
        action = (
            "Review downstream tasks and evaluate schedule mitigation "
            "options."
        )
    else:
        risk = "MEDIUM"
        decision = "ESCALATE"
        reason = (
            f"The observed delay ({delay} days) exceeds the available "
            f"project buffer ({buffer} days)."
        )
        action = "Investigate the delay and evaluate schedule mitigation options."

    return {
        "task": update["task"],
        "risk_level": risk,
        "decision": decision,
        "reason": reason,
        "recommended_action": action,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Rule-based Schedule Risk Escalation baseline."
    )
    parser.add_argument("--input", required=True, help="Path to schedule update JSON")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        update = json.load(f)

    result = assess_schedule_risk(update)

    print("Schedule Risk Assessment")
    print("========================")
    print(f"Task: {result['task']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Decision: {result['decision']}")
    print()
    print(f"Reason: {result['reason']}")
    print()
    print(f"Recommended Action: {result['recommended_action']}")


if __name__ == "__main__":
    main()
