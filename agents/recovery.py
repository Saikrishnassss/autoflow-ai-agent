def recover(issues):
    for task in issues:
        task["attempts"] += 1

        if task["attempts"] == 1:
            task["status"] = "retrying"
            task["history"].append(
                "Retry triggered because task failed on first attempt"
            )

        elif task["attempts"] >= 2:
            task["status"] = "escalated"

            # 🔥 Only assign Manager if owner is unknown
            if task["owner"] == "unknown":
                task["owner"] = "Manager"

            task["history"].append(
                "Escalated because repeated failures indicate risk of SLA breach"
            )

    return issues