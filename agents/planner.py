def create_plan(tasks):
    workflow = []

    for i, t in enumerate(tasks):
        owner = t.get("owner", "")

        if not owner:
            status = "needs_clarification"
        else:
            status = "pending"

        workflow.append({
            "id": i,
            "task": t.get("task", ""),
            "owner": owner if owner else "unknown",
            "deadline": t.get("deadline", ""),
            "status": status,
            "attempts": 0,
            "history": []
        })

    return workflow