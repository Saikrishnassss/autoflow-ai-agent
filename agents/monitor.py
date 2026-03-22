def monitor(workflow):
    issues = []

    for task in workflow:
        if task["status"] == "failed":
            task["history"].append(
                "Failure detected → risk of SLA breach, triggering recovery workflow"
            )
            issues.append(task)

    return issues