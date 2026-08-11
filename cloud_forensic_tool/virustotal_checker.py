import requests
import os

# Load VirusTotal API key from environment variable.
# Get your API key from https://www.virustotal.com/gui/my-apikey
# Copy .env.example to .env and set VIRUSTOTAL_API_KEY.
API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", "your_virustotal_api_key_here")


def check_file_hash_virustotal(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        stats = result["data"]["attributes"]["last_analysis_stats"]

        if stats["malicious"] > 0:
            return "Malware Detected"
        elif stats["suspicious"] > 0:
            return "Suspicious File"
        else:
            return "Clean"

    return "Not Found"