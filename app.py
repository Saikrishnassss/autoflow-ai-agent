from agents.understanding import extract_tasks
from agents.planner import create_plan
from agents.executor import execute
from agents.monitor import monitor
from agents.recovery import recover
import datetime


# ✅ Enterprise-style audit logging
def log_event(event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {event}"

    print("AUDIT:", entry)

    with open("logs/audit.log", "a") as f:
        f.write(entry + "\n")


def run_system(meeting_text):
    log_event("SYSTEM STARTED")

    # =========================
    # 🧠 Understanding Phase
    # =========================
    print("\n=== Understanding Phase ===")
    tasks = extract_tasks(meeting_text)
    print("Extracted Tasks:", tasks)

    # =========================
    # 🧩 Planning Phase
    # =========================
    print("\n=== Planning Phase ===")
    workflow = create_plan(tasks)

    # =========================
    # ⚠️ Clarification Handling
    # =========================
    print("\n=== Clarification Phase ===")
    for task in workflow:
        if task["status"] == "needs_clarification":
            print(f"\n[Understanding Agent] Missing owner detected → task: {task['task']}")
            print("[Planning Agent] Assigning fallback owner → Manager")

            task["owner"] = "Manager"
            task["status"] = "pending"
            task["history"].append("Owner auto-assigned by system (fallback)")

    # =========================
    # 🔁 Execution Loop
    # =========================
    all_done = False

    while not all_done:

        # 🚀 Execution Phase
        print("\n=== Execution Phase ===")
        workflow = execute(workflow)

        # 📊 Monitoring Phase
        print("\n=== Monitoring Phase ===")
        issues = monitor(workflow)

        # 🔥 SLA Detection (FIXED)
        for task in workflow:
            if (
                "urgent" in task["task"].lower()
                or "immediate" in task.get("deadline", "").lower()
            ):
                if "High SLA risk detected → priority handling enabled" not in task["history"]:
                    task["history"].append("High SLA risk detected → priority handling enabled")

        # 🔁 Recovery Phase
        if issues:
            print("\n=== Recovery Phase ===")
            print("[Recovery Agent] Failure detected → initiating retry / escalation strategy")
            recover(issues)

        # ✅ Check completion
        all_done = all(
            t["status"] in ["completed", "escalated", "needs_clarification"]
            for t in workflow
        )

        # 🛑 Prevent infinite loop
        for t in workflow:
            if t["status"] == "retrying":
                t["status"] = "failed"

    log_event("SYSTEM COMPLETED")
    return workflow


# =========================
# ▶️ MAIN ENTRY (Demo Mode)
# =========================
if __name__ == "__main__":
    meeting_text = (
        "John will prepare report by Monday. "
        "Alice will update dashboard urgently by Wednesday. "
        "Team needs to review budget by Friday. "
        "There is a pending approval stuck for 48 hours that needs immediate action."
    )

    result = run_system(meeting_text)

    print("\n=========================")
    print("🚀 FINAL WORKFLOW OUTPUT")
    print("=========================\n")

    for r in result:
        print(f"Task   : {r['task']}")
        print(f"Owner  : {r['owner']}")
        print(f"Status : {r['status']}")
        print("History:")
        for h in r["history"]:
            print(f"  - {h}")
        print("-" * 40)