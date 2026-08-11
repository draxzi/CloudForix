import requests
import os

# Load Azure Bearer token from environment variable.
# In production, use MSAL to acquire tokens dynamically — see ms_graphs_log.py.
# Copy .env.example to .env and set AZURE_ACCESS_TOKEN.
# See SECURITY.md — never hardcode tokens in source files.
ACCESS_TOKEN = os.environ.get("AZURE_ACCESS_TOKEN", "your_azure_bearer_token_here")


def collect_onedrive_logs():
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }

    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_file = "logs/onedrive_logs.txt"
        with open(log_file, "w") as f:
            if "value" in data:
                for item in data["value"]:
                    f.write(f"{item['name']} - {item['lastModifiedDateTime']}\n")
            else:
                f.write("No OneDrive logs found\n")

        print("OneDrive logs collected")
        return log_file

    except Exception as e:
        print("OneDrive API error:", e)
        return None