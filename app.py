import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from agents.understanding import extract_tasks
from agents.planner import create_plan
from agents.executor import execute
from agents.monitor import monitor
from agents.recovery import recover
from agents.audit import log_event

load_dotenv()

app = Flask(__name__, static_folder="static")
CORS(app)

def run_system_logic(meeting_text: str, scenario: str, human_override: str = None):
    execution_logs = []
    
    def emit_log(msg):
        print(msg)
        execution_logs.append(msg)
    
    emit_log(f"🚀 Initializing workflow for scenario: {scenario}")
    log_event("Workflow_Started", f"Executing Hackathon Scenario: {scenario}")

    # --- 1. Understanding Phase ---
    emit_log("\n[AGENT: Understanding] Extracting tasks from input text...")
    tasks = extract_tasks(meeting_text)
    emit_log(f" -> Found {len(tasks)} tasks.")
    log_event("Tasks_Extracted", f"Found {len(tasks)} tasks.", raw_json=str(tasks))

    # --- 2. Planning Phase ---
    emit_log("\n[AGENT: Planning] Formulating execution workflow...")
    workflow = create_plan(tasks)
    emit_log(f" -> Plan initialized with {len(workflow)} nodes.")
    log_event("Plan_Created", f"Plan initialized.", raw_json=str(workflow))

    # --- 3. Clarification / Human-in-loop ---
    emit_log("\n[AGENT: Clarification] Checking for ambiguities...")
    for task in workflow:
        if task["status"] == "needs_clarification":
            emit_log(f" ⚠️ [Human-in-the-Loop] Ambiguous Task Detected: '{task['task']}'")
            emit_log(" -> The agent could not identify an owner.")
            
            override_val = human_override if human_override else "Manager"
            emit_log(f" -> Applying external override: Assigned to '{override_val}'")
            
            task["owner"] = override_val
            task["status"] = "pending"
            task["history"].append("Owner clarified by human override")
            log_event("Clarification_Override", f"Task '{task['task']}' assigned to {override_val}")

    # --- 4. Execution & Self-Healing Loop ---
    all_done = False
    loop_count = 0
    max_loops = 5

    while not all_done and loop_count < max_loops:
        loop_count += 1
        emit_log(f"\n--- Execution Loop [{loop_count}] ---")
        
        # Execute
        emit_log("[AGENT: Executor] Running pending tasks...")
        workflow = execute(workflow, scenario)

        # Monitor
        emit_log("[AGENT: Monitor] Scanning for failures or SLA breaches...")
        issues = monitor(workflow, scenario)

        # Recover
        if issues:
            emit_log(f" 🚨 [AGENT: Monitor] Detected {len(issues)} issues! Triggering Recovery.")
            log_event("Monitor_Alert", f"Detected {len(issues)} issues.", raw_json=str([i['task'] for i in issues]))
            
            emit_log("[AGENT: Recovery] Analyzing failures with LLM and determining strategy...")
            workflow = recover(issues) # Recovery updates the workflow objects in place
            log_event("Recovery_Executed", f"Recovery applied logic.")
            
            for iss in issues:
                emit_log(f" -> Recovery set status to: {iss['status']} for task '{iss['task']}'")

        # Check completion
        all_done = all(
            t["status"] in ["completed", "escalated", "rerouted", "needs_clarification"]
            for t in workflow
        )

    emit_log("\n✅ Workflow execution cycle finished.")
    
    # --- 5. Workflow Wrap-up / Completion ---
    from agents.reporter import generate_report
    emit_log("\n[AGENT: Reporter] Generating Final Workflow Completion Payload...")
    final_report = generate_report(workflow, scenario)
    
    emit_log(" -> Enterprise Completion Report Generated (Simulated Webhook Dispatched).")
    emit_log("\n--- REPORT ---")
    
    # Truncate lines carefully to not overwhelm UI
    for line in final_report.split("\n"):
        emit_log(f"   {line}")
        
    emit_log("--------------\n")

    log_event("Workflow_Completed", "Execution loop finished successfully. Final Report generated via LLM.")
    
    return {"workflow": workflow, "logs": execution_logs}

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.json
    if not data or "text" not in data or "scenario" not in data:
        return jsonify({"error": "Missing 'text' or 'scenario' in request"}), 400

    if not os.getenv("GROQ_API_KEY"):
        return jsonify({
            "error": "Backend Configuration Error",
            "logs": ["ERROR: GROQ_API_KEY not found in server environment variables. Please configure it in Render to run the Groq Llama-3 model."]
        }), 500

    try:
        result = run_system_logic(
            meeting_text=data["text"],
            scenario=data["scenario"],
            human_override=data.get("override", "Manager")
        )
        return jsonify(result)
    except Exception as e:
        log_event("System_Fault", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/api/audit", methods=["GET"])
def api_audit():
    # Return the last 50 lines of the audit log
    if not os.path.exists("logs/audit.log"):
        return jsonify({"logs": []})
        
    with open("logs/audit.log", "r") as f:
        lines = f.readlines()
    return jsonify({"logs": lines[-50:]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)