import datetime
import os

def log_event(event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = f"[{timestamp}] {event}"

    print("AUDIT:", log_message)

    # Ensure logs folder exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open("logs/audit.log", "a") as f:
        f.write(log_message + "\n")