def detect_attacks(log_file):
    alerts = []
    with open(log_file, "r", errors="ignore") as f:
        data = f.read().lower()

        if "failed login" in data:
            alerts.append("Brute Force Attempt Detected")

        if "unauthorized" in data:
            alerts.append("Unauthorized Access Detected")

        if "malware" in data:
            alerts.append("Malware Detected")

    return alerts