import os
import subprocess
from datetime import datetime

def collect_dns_logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file = "logs/dns_logs.txt"

    with open(log_file, "w") as f:
        f.write("===== DNS LOGS =====\n")
        f.write("Log Time: " + str(datetime.now()) + "\n\n")

        try:
            dns_logs = subprocess.getoutput("ipconfig /displaydns")
            f.write(dns_logs)
        except Exception as e:
            f.write("Error collecting DNS logs: " + str(e))

    print("DNS logs collected")
    return log_file