def create_plan(tasks: list) -> list:
    workflow = []
    
    for i, t in enumerate(tasks):
        owner = t.get("owner", "").strip()
        
        # If the LLM left the owner empty, flag for clarification
        if not owner:
            status = "needs_clarification"
        else:
            status = "pending"
            
        workflow.append({
            "id": i,
            "task": t.get("task", ""),
            "owner": owner if owner else "unknown",
            "deadline": t.get("deadline", ""),
            "priority": t.get("priority", "medium"),
            "status": status,
            "attempts": 0,
            "history": []
        })
        
    return workflow