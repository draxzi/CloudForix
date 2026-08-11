def collect_aws_logs():
    with open("logs/aws_logs.txt", "w") as f:
        f.write("User login successful\n")
        f.write("Failed login attempt from IP 192.168.1.10\n")
        f.write("Failed login attempt from IP 192.168.1.10\n")
        f.write("Unauthorized access attempt detected\n")
        f.write("New admin account created\n")
        f.write("File uploaded to cloud storage\n")
        f.write("Unknown process started: trojan.exe\n")
        f.write("Access denied for user guest\n")
        f.write("SSH login failed from IP 10.10.10.5\n")
    print("AWS Logs Collected (Simulated)")

def collect_azure_logs():
    with open("logs/azure_logs.txt", "w") as f:
        f.write("User login successful\nAccess denied\n")
    print("Azure Logs Collected")

def collect_onedrive_logs():
    with open("logs/onedrive_logs.txt", "w") as f:
        f.write("Unauthorized access attempt detected\nNew admin account created\n")
    print("OneDrive Logs Collected")

def collect_google_drive_logs():
    with open("logs/google_logs.txt", "w") as f:
        f.write("Failed login attempt\nUnknown process started\n")
    print("Google Drive Logs Collected")

def collect_all_cloud_logs():
    collect_aws_logs()
    collect_azure_logs()
    collect_onedrive_logs()
    collect_google_drive_logs()