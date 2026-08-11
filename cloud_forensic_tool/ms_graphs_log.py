import requests
import msal
import json
import os

# Load Azure credentials from environment variables.
# Copy .env.example to .env and fill in your real values.
# See SECURITY.md — never hardcode credentials in source files.
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "your_azure_client_id_here")
TENANT_ID = os.environ.get("AZURE_TENANT_ID", "your_azure_tenant_id_here")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "your_azure_client_secret_here")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

def get_access_token():
    try:
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET,
        )

        token = app.acquire_token_for_client(scopes=SCOPE)

        if "access_token" in token:
            return token['access_token']
        else:
            print("Token error:", token)
            return None

    except Exception as e:
        print("Authentication error:", e)
        return None


def collect_ms_logs():
    token = get_access_token()
    if not token:
        print("Microsoft login failed")
        return

    headers = {
        'Authorization': 'Bearer ' + token
    }

    try:
        # Sign-in logs
        signin_url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
        signin_response = requests.get(signin_url, headers=headers)

        with open("logs/ms_signin_logs.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(signin_response.json(), indent=4))

        # OneDrive activity logs
        drive_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
        drive_response = requests.get(drive_url, headers=headers)

        with open("logs/onedrive_activity_logs.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(drive_response.json(), indent=4))

        print("Microsoft Cloud Logs Collected")

    except Exception as e:
        print("Microsoft log collection failed:", e)