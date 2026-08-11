import os
import subprocess
from datetime import datetime

def collect_network_logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file = "logs/network_logs.txt"

    with open(log_file, "w") as f:
        f.write("===== NETWORK LOGS =====\n")
        f.write("Log Time: " + str(datetime.now()) + "\n\n")

        try:
            # Active connections
            f.write("---- ACTIVE CONNECTIONS ----\n")
            connections = subprocess.getoutput("netstat -ano")
            f.write(connections + "\n\n")

            # ARP table (connected devices)
            f.write("---- ARP TABLE ----\n")
            arp = subprocess.getoutput("arp -a")
            f.write(arp + "\n\n")

            # Routing table
            f.write("---- ROUTE TABLE ----\n")
            route = subprocess.getoutput("route print")
            f.write(route + "\n\n")

        except Exception as e:
            f.write("Error collecting network logs: " + str(e))

    print("Network logs collected")
    return log_file