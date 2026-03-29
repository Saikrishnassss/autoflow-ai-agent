import os
import json
from agents.llm_config import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

def recover(issues: list) -> list:
    llm = get_llm()
    system_prompt = """
    You are the AutoFlow AI Recovery Agent. Your job is to analyze failed or stalled tasks and output an exact JSON string containing your decision on how to handle the error.
    
    You must choose ONE of the following precise JSON responses, deciding between RETRY, REROUTE (delegate), or ESCALATE (support):
    
    IF the error involves an 'approver on leave' or a bottleneck needing a delegate:
    {"decision": "reroute", "action": "Reassigned to alternate delegate/manager", "owner_update": "Delegate_Manager"}
    
    IF the error is an API failure (like JIRA) and the number of attempts is 0 or 1:
    {"decision": "retry", "action": "Triggered automated retry sequence"}
    
    IF the error is an API failure (like JIRA) and the number of attempts >= 1 (it failed again):
    {"decision": "escalate", "action": "Escalated to IT Support for manual intervention"}
    
    Only reply with the raw JSON. Nothing else.
    """
    
    for task in issues:
        # Extract task history for LLM context
        error_context = " | ".join(task["history"])
        attempts = task.get("attempts", 0)
        
        user_prompt = f"Task: {task['task']}\nStatus: {task['status']}\nAttempts so far: {attempts}\nError History: {error_context}\nDetermine recovery strategy in JSON format."
        
        try:
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            # Very basic cleanup incase the model outputs markdown backticks
            raw_text = response.content.strip().replace("```json", "").replace("```", "")
            decision_data = json.loads(raw_text)
            
            task["attempts"] = attempts + 1
            decision = decision_data.get("decision", "escalate")
            
            if decision == "retry":
                task["status"] = "retrying"
                task["history"].append(f"[Recovery Agent] {decision_data.get('action')}")
                
            elif decision == "reroute":
                task["status"] = "rerouted"
                if decision_data.get("owner_update"):
                    task["owner"] = decision_data["owner_update"]
                task["history"].append(f"[Recovery Agent] {decision_data.get('action')}")
                
            elif decision == "escalate":
                task["status"] = "escalated"
                task["history"].append(f"[Recovery Agent] {decision_data.get('action')}")
                
        except Exception as e:
            print(f"Recovery LLM Error: {e}")
            task["status"] = "escalated"
            task["history"].append(f"Fallback Escalate due to LLM reasoning failure: {e}")

    return issues