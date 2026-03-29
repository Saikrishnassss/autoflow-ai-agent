def execute(workflow):
    for task in workflow:

        if task["status"] not in ["pending", "retrying"]:
            continue

        task_name = task["task"].lower()

        # SLA-aware failure simulation
        if any(word in task_name for word in ["urgent", "dashboard", "review"]):
            task["status"] = "failed"
            task["history"].append(
                "Execution failed → high SLA risk task (urgent/complex)"
            )
            task["history"].append("Simulated API call → Task execution service")

        else:
            task["status"] = "completed"
            task["history"].append(
                "Task completed successfully without SLA risk"
            )

    return workflow