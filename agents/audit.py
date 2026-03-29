import os
import datetime
import json

def log_event(event_type: str, details: str, raw_json: str = None):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file = "logs/audit.log"
    
    # Ensure log file exists
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("=== AutoFlow AI Enterprise Audit Log ===\n")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    entry = f"[{timestamp}] [{event_type.upper()}] {details}"
    if raw_json:
        entry += f"\n  -> Metadata: {raw_json}"
        
    print(f"AUDIT TRAIL: {entry}")

    with open(log_file, "a") as f:
        f.write(entry + "\n")