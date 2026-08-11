import os
import re
from datetime import datetime

def extract_metadata(file_path):
    metadata = {
        "file_name": os.path.basename(file_path),
        "file_size": 0,
        "created_time": "",
        "modified_time": "",
        "accessed_time": "",
        "ip_addresses": [],
        "emails": [],
        "timestamps": [],
        "activities": [],
        "failed_logins": {},
        "successful_logins": {}
    }

    try:
        # File size
        metadata["file_size"] = os.path.getsize(file_path)

        # MAC Times (Created, Modified, Accessed)
        stat = os.stat(file_path)
        metadata["created_time"] = datetime.fromtimestamp(stat.st_ctime).isoformat()
        metadata["modified_time"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
        metadata["accessed_time"] = datetime.fromtimestamp(stat.st_atime).isoformat()

        # Read file content
        with open(file_path, "r", errors="ignore") as f:
            data = f.read().lower()

            # Extract IP addresses
            metadata["ip_addresses"] = list(set(
                re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)
            ))

            # Extract Emails
            metadata["emails"] = list(set(
                re.findall(r'[\w\.-]+@[\w\.-]+', data)
            ))

            # Extract timestamps from logs
            metadata["timestamps"] = list(set(
                re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', data)
            ))

            # Detect activities
            keywords = [
                "login", "logon", "failed", "success",
                "download", "upload", "delete",
                "access", "created", "modified"
            ]

            for word in keywords:
                if word in data:
                    metadata["activities"].append(word)

            # Failed login detection with IP
            failed_matches = re.findall(
                r'failed.*?(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)', data
            )

            for ip in failed_matches:
                metadata["failed_logins"][ip] = metadata["failed_logins"].get(ip, 0) + 1

            # Successful login detection with IP
            success_matches = re.findall(
                r'success.*?(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)', data
            )

            for ip in success_matches:
                metadata["successful_logins"][ip] = metadata["successful_logins"].get(ip, 0) + 1

    except Exception as e:
        print("Metadata extraction error:", e)

    return metadata