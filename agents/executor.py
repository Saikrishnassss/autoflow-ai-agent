import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.llm_config import get_llm

MOCK_ENVIRONMENT = """
[CURRENT SIMULATED INFRASTRUCTURE STATE]
- JIRA API (Atlassian): OFFLINE (HTTP 403 Forbidden - SSL Cert Expired)
- Slack Webhook API: ONLINE (HTTP 200 OK)
- Internal Email Exchange: ONLINE (HTTP 200 OK)
- HR Leave Management System: Manager 'Bob' is on Vacation (Approval Queue Stalled for 72h)
"""

def execute(workflow: list, scenario: str = "") -> list:
    llm = get_llm()
    
    system_prompt = f"""
    You are the AutoFlow Executor Agent. Your job is to physically execute enterprise tasks.
    Because you are running in a sandbox, you will 'simulate' the execution by querying the environment state and formulating a JSON simulation response.
    
    {MOCK_ENVIRONMENT}
    
    You MUST output valid JSON with this exact schema:
    {{
      "status": "completed" | "failed",
      "transaction_log": "Simulated terminal output of the API transaction attempt",
      "http_code": 200 | 403 | 500,
      "latency_ms": 120
    }}
    
    If the task requires a system that is OFFLINE or Stalled, you MUST output 'failed'.
    If it requires a system that is ONLINE, you MUST output 'completed'.
    Output only the JSON block, no markdown formatting.
    """
    
    for task in workflow:
        if task["status"] not in ["pending", "retrying"]:
            continue
            
        try:
            user_msg = f"Task: {task['task']}\nAttempts so far: {task['attempts']}\nScenario Context: {scenario}"
            
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_msg)
            ])
            
            raw_text = response.content.strip().replace("```json", "").replace("```", "")
                
            execution_data = json.loads(raw_text)
            
            sim_status = execution_data.get("status", "failed")
            task["status"] = sim_status
            task["history"].append(f"[Executor Agent] HTTP {execution_data.get('http_code', '500')} | Latency: {execution_data.get('latency_ms', 0)}ms -> {execution_data.get('transaction_log', 'Connection Attempted')}")
            
        except Exception as e:
            print(f"Executor LLM Simulation Error: {e}")
            task["status"] = "failed"
            task["history"].append(f"[Executor Agent] Execution failed systemically: LLM Parsing Exception - {e}")

    return workflow