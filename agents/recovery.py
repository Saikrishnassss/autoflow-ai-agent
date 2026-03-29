def recover(issues):
    for task in issues:
        task["attempts"] += 1

        # First retry attempt
        if task["attempts"] == 1:
            task["status"] = "retrying"
            task["history"].append(
                "Retry triggered → automated recovery attempt initiated"
            )
            task["history"].append(
                "Simulated system action → retrying via workflow engine"
            )

        # Escalation after repeated failure
        elif task["attempts"] >= 2:
            task["status"] = "escalated"

            # Assign fallback owner only if unknown
            if task["owner"] == "unknown":
                task["owner"] = "Manager"

            task["history"].append(
                "Escalated due to repeated failures → SLA breach risk identified"
            )
            task["history"].append(
                "Notification sent to manager (simulated email/Slack alert)"
            )

    return issues