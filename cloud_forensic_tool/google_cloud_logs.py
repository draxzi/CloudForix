from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os
from datetime import datetime

SCOPES = ['openid',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.activity.readonly']

def collect_google_drive_logs():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(pageSize=20, fields="files(name, modifiedTime)").execute()
    files = results.get('files', [])

    if not os.path.exists("logs"):
        os.makedirs("logs")

    filename = "logs/google_drive_logs_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

    with open(filename, "w") as f:
        for file in files:
            f.write(f"File: {file['name']} | Modified: {file['modifiedTime']}\n")

    print("Google Drive logs collected")
    return filename