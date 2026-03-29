import json
from langchain_core.messages import SystemMessage, HumanMessage
from agents.llm_config import get_llm

def generate_report(workflow: list, scenario: str = "") -> str:
    """
    Generates a formal completion payload to wrap up the execution cycle.
    """
    llm = get_llm()
    
    # Extract minimal context to save tokens
    summary_data = [{"task": t["task"], "final_status": t["status"], "owner": t["owner"]} for t in workflow]
    
    system_prompt = """
    You are the AutoFlow Reporting Agent. Your role is the final step of the pipeline.
    You analyze the finalized workflow data and return a professional final summary Report detailing the process completion.
    
    Include:
    1. An executive summary of the overall scenario resolution.
    2. A brief list of tasks and whether they were Automated successfully or required Escaping/Escalating.
    3. A clear 'Workflow Execution Completed successfully' closing statement.
    
    Keep it extremely tight and professional. Output plain text/markdown.
    """
    
    user_msg = f"Scenario: {scenario}\nFinal State: {json.dumps(summary_data, indent=2)}\n\nGenerate the Final Enterprise Completion Report."
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_msg)
        ])
        return response.content.strip()
    except Exception as e:
        print(f"Reporting LLM Error: {e}")
        return "⚠️ Automated Reporting Failed due to an LLM exception. Raw workflow outputs have been natively logged to DB."
