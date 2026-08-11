import os
import subprocess
from datetime import datetime

def collect_system_logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file = "logs/system_logs.txt"

    with open(log_file, "w") as f:
        f.write("===== SYSTEM LOGS =====\n")
        f.write("Log Time: " + str(datetime.now()) + "\n\n")

        try:
            # Login events
            f.write("---- LOGIN EVENTS ----\n")
            login_logs = subprocess.getoutput(
                'wevtutil qe Security "/q:*[System[(EventID=4624 or EventID=4625)]]" /f:text /c:5'
            )
            f.write(login_logs + "\n\n")

            # Account events
            f.write("---- ACCOUNT EVENTS ----\n")
            account_logs = subprocess.getoutput(
                'wevtutil qe Security "/q:*[System[(EventID=4720 or EventID=4726)]]" /f:text /c:5'
            )
            f.write(account_logs + "\n\n")

            # Process creation
            f.write("---- PROCESS EVENTS ----\n")
            process_logs = subprocess.getoutput(
                'wevtutil qe Security "/q:*[System[(EventID=4688)]]" /f:text /c:5'
            )
            f.write(process_logs + "\n\n")

        except Exception as e:
            f.write("Error collecting system logs: " + str(e))

    print("System logs collected")
    return log_file