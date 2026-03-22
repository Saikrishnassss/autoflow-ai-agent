from agents.understanding import extract_tasks
from agents.planner import create_plan
from agents.executor import execute
from agents.monitor import monitor
from agents.recovery import recover
from agents.audit import log_event


def run_system(meeting_text):
    log_event("START")

    tasks = extract_tasks(meeting_text)
    print("RAW TASK OUTPUT:", tasks)

    workflow = create_plan(tasks)
# 🔥 ADD THIS BLOCK HERE
    for task in workflow:
        if task["status"] == "needs_clarification":
            print(f"\nClarification needed for task: {task['task']}")
            new_owner = input("Enter owner: ")
            task["owner"] = new_owner
            task["status"] = "pending"
            task["history"].append("Owner provided by user after clarification")

 
    all_done = False

    while not all_done:
        workflow = execute(workflow)
        issues = monitor(workflow)

        if issues:
            recover(issues)

        all_done = all(
            t["status"] in ["completed", "escalated", "needs_clarification"]
            for t in workflow
        )

        # prevent infinite loop
        for t in workflow:
            if t["status"] == "retrying":
                t["status"] = "failed"

    log_event("END")
    return workflow


if __name__ == "__main__":
    meeting_text = input("Enter meeting notes:\n")

    result = run_system(meeting_text)

    print("\nFinal Workflow:\n")
    for r in result:
        print("\nTask:", r["task"])
        print("Owner:", r["owner"])
        print("Status:", r["status"])
        print("History:", r["history"])