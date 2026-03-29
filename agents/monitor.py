def monitor(workflow: list, scenario: str = "") -> list:
    issues = []
    
    for task in workflow:
        # 1. Detect Standard Execution Failures
        if task["status"] == "failed":
            task["history"].append("Monitor detected failure -> Routing to Recovery workflow")
            issues.append(task)
            continue
            
        # 2. SLA Breach Scenario Simulator (Track 2 Scenario 3 - SLA Breach Prevention)
        if scenario == "sla_breach" and task["status"] == "pending":
            if "approval" in task["task"].lower():
                # Inject a 48-hour stalled timer
                task["status"] = "stalled"
                task["history"].append("🚨 MONITOR ALERT: Task SLA Breach Risk! Found approval stuck for 48 hours. Identifying bottleneck: Approver is on leave. Routing to Recovery.")
                issues.append(task)
                continue
                
    return issues