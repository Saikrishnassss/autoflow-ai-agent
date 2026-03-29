import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.llm_config import get_llm

def monitor(workflow: list, scenario: str = "") -> list:
    llm = get_llm()
    issues = []
    
    system_prompt = """
    You are the AutoFlow Monitor Agent. You analyze execution traces and detect failures, security blocks, or SLA breaches.
    Review the provided task's execution history. 
    
    Output JSON with this exact schema:
    {
      "issue_detected": true or false,
      "issue_type": "None" | "Hardware Failure" | "API Error" | "SLA Stalled",
      "reasoning": "A 1-sentence explanation of why an issue was or was not detected."
    }
    
    If the history shows HTTP 403 or 500, or explicitly states 'failed', that is an 'API Error'.
    If the history shows an approval waiting on a Manager who is on vacation, that is an 'SLA Stalled'.
    If the history shows HTTP 200 OK, there is NO issue.
    Output only raw JSON, no markdown formatting ticks.
    """
    
    for task in workflow:
        if task["status"] in ["completed", "rerouted", "escalated"]:
            continue
            
        try:
            history_text = " | ".join(task["history"][-2:])
            user_msg = f"Task: {task['task']}\nCurrent Execution State: {task['status']}\nRecent History Logs: {history_text}\nScenario: {scenario}"
            
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_msg)
            ])
            
            raw_text = response.content.strip().replace("```json", "").replace("```", "")
                
            monitor_data = json.loads(raw_text)
            
            if monitor_data.get("issue_detected"):
                task["history"].append(f"🚨 [Monitor Alert]: {monitor_data.get('issue_type')} - {monitor_data.get('reasoning')}")
                issues.append(task)
                
        except Exception as e:
            print(f"Monitor LLM Analysis Error: {e}")
            # Fallback to deterministic generic error if LLM fails
            if task["status"] == "failed":
                task["history"].append("🚨 [Monitor Alert]: Generic system failure detected.")
                issues.append(task)

    return issues