import random

def execute(workflow: list, scenario: str = "") -> list:
    for task in workflow:
        if task["status"] not in ["pending", "retrying"]:
            continue

        task_name = task["task"].lower()
        
        # Determine success / failure based on the scenario we are simulating
        
        # Scenario 1 (Track 2): Employee Onboarding -> simulating JIRA access error
        if scenario == "employee_onboarding":
            if "jira" in task_name or "system" in task_name or "account" in task_name:
                # Force failure if it's the first attempt
                if task["attempts"] == 0:
                    task["status"] = "failed"
                    task["history"].append("Execution failed: JIRA API Access Error (HTTP 403 Forbidden)")
                else:
                    # Fail again on retry to trigger escalation logic to IT
                    task["status"] = "failed"
                    task["history"].append("Execution failed: JIRA API Access Error persists after retry")
                continue
        
        # If it passes scenario constraints or is another task, execute properly
        task["status"] = "completed"
        task["history"].append(f"Task executed successfully (Simulated API call)")
        
    return workflow