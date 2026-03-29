def extract_tasks(text):
    tasks = []

    text = text.lower()

    if "report" in text:
        tasks.append({
            "task": "prepare report",
            "owner": "John",
            "deadline": "Monday"
        })

    if "dashboard" in text:
        tasks.append({
            "task": "update dashboard",
            "owner": "Alice",
            "deadline": "Wednesday"
        })

    if "review budget" in text:
        tasks.append({
            "task": "review budget",
            "owner": "",
            "deadline": "Friday"
        })

    if "approval" in text:
        tasks.append({
            "task": "approval for pending procurement task",
            "owner": "",
            "deadline": "immediately"
        })

    return tasks