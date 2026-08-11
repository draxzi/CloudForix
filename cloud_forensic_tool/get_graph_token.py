import requests
import os

# Load Azure credentials from environment variables.
# Copy .env.example to .env and fill in your real values.
# See SECURITY.md — never hardcode credentials in source files.
tenant_id = os.environ.get("AZURE_TENANT_ID", "your_azure_tenant_id_here")
client_id = os.environ.get("AZURE_CLIENT_ID", "your_azure_client_id_here")
client_secret = os.environ.get("AZURE_CLIENT_SECRET", "your_azure_client_secret_here")

url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

data = {
    "client_id": client_id,
    "scope": "https://graph.microsoft.com/.default",
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

response = requests.post(url, data=data)
token = response.json().get("access_token")

print("ACCESS TOKEN:\n")
print(token)