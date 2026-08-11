import requests
import os

# Load Azure Bearer token from environment variable.
# In production, use MSAL to acquire tokens dynamically — see ms_graphs_log.py.
# Copy .env.example to .env and set AZURE_ACCESS_TOKEN.
# See SECURITY.md — never hardcode tokens in source files.
ACCESS_TOKEN = os.environ.get("AZURE_ACCESS_TOKEN", "your_azure_bearer_token_here")


def collect_mde_logs():
    url = "https://graph.microsoft.com/v1.0/security/alerts"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_file = "logs/mde_logs.txt"

        with open(log_file, "w") as f:
            if "value" in data:
                for alert in data["value"]:
                    f.write("Alert: " + str(alert.get("title", "Unknown")) + "\n")
                    f.write("Severity: " + str(alert.get("severity", "Unknown")) + "\n")
                    f.write("User: " + str(alert.get("userStates", "")) + "\n")
                    f.write("Time: " + str(alert.get("createdDateTime", "")) + "\n")
                    f.write("Description: " + str(alert.get("description", "")) + "\n")
                    f.write("------------------------------------------------\n")

        print("MDE logs collected")
        return log_file

    except Exception as e:
        print("MDE log error:", e)
        return None