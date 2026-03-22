def execute(workflow):
    for task in workflow:

        if task["status"] not in ["pending", "retrying"]:
            continue

        task_name = task["task"].lower()

        # 🔥 SLA + risk-aware execution
        if "urgent" in task_name or "dashboard" in task_name or "review" in task_name:
            task["status"] = "failed"
            task["history"].append(
                "Execution failed due to high-risk task (urgent/complex), potential SLA impact"
            )

        else:
            task["status"] = "completed"
            task["history"].append(
                "Task completed successfully without risk"
            )

    return workflow